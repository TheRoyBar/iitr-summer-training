"""
The BiLSTM/Siamese model itself is not directly interpretable, so
this module adds a simple keyword-overlap layer on top of the raw
text purely to give the user a human-readable "why" alongside the
model's prediction. This does not feed into the model in any way.

Skill vocabulary is loaded from data/skill_vocab.json, which is
built by make_dataset.py from the real 'Skills' field in the source
dataset (the 800 most common skill phrases).
"""

import json
import os
import re

_VOCAB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "skill_vocab.json")

_cached_skills = None


def _load_skills():
    global _cached_skills
    if _cached_skills is None:
        with open(_VOCAB_PATH, "r", encoding="utf-8") as f:
            skills = json.load(f)
        # sort longest-first so multi-word skills (e.g. "problem-solving skills")
        # are matched before their shorter substrings
        _cached_skills = sorted(skills, key=len, reverse=True)
    return _cached_skills


def extract_skills(text):
    text = text.lower()
    found = set()
    for skill in _load_skills():
        # word-boundary match so short skills like "r", "c", "ui" don't
        # match inside unrelated words (e.g. "r" inside "career")
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(skill)
    return found


def skill_overlap_report(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    common = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)

    return {
        "common_skills": common,
        "missing_skills": missing,
    }
