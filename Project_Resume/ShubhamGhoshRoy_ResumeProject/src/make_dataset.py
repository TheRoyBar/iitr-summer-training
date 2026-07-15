"""
Builds data/resume_jd_dataset.csv from the real train_raw.jsonl file.

Each source row has one Job-Description plus a Resume-matched (the
resume actually hired/shortlisted for that JD) and a Resume-unmatched
(the same candidate's resume with several key skills missing, see
the 'Skills' field). That structure maps naturally onto three classes:

  Strong (2): JD paired with its own Resume-matched
              -> full skill overlap, real positive pair
  Medium (1): JD paired with its own Resume-unmatched
              -> same candidate/domain but missing skills, partial overlap
  Weak   (0): JD paired with a Resume-matched pulled from a different,
              randomly chosen row -> unrelated domain, near-zero overlap

This keeps every pair grounded in real text instead of templates,
while still giving three well-separated classes to train on.
"""

import json
import csv
import random

random.seed(42)

RAW_PATH = "data/train_raw.jsonl"
OUT_PATH = "data/resume_jd_dataset.csv"
N_SOURCE_ROWS = 3000   # rows sampled from the 50k source file (x3 for 9k pairs)


def load_rows(path=RAW_PATH, n=N_SOURCE_ROWS):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    random.shuffle(rows)
    return rows[:n]


def build_dataset(n_source_rows=N_SOURCE_ROWS, out_path=OUT_PATH):
    rows = load_rows(n=n_source_rows)

    pairs = []
    skill_counts = {}
    for i, row in enumerate(rows):
        jd = row["Job-Description"].strip()
        matched = row["Resume-matched"].strip()
        unmatched = row["Resume-unmatched"].strip()

        # strong: JD + its true matched resume
        pairs.append((matched, jd, 2))

        # medium: JD + its own unmatched (partial-skill) resume
        pairs.append((unmatched, jd, 1))

        # weak: JD + a matched resume from a random different row
        other_idx = random.choice([j for j in range(len(rows)) if j != i])
        other_resume = rows[other_idx]["Resume-matched"].strip()
        pairs.append((other_resume, jd, 0))

        for s in row.get("Skills", []):
            s = s.strip().lower()
            if s:
                skill_counts[s] = skill_counts.get(s, 0) + 1

    random.shuffle(pairs)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["resume_text", "job_description", "match_label"])
        writer.writerows(pairs)

    # save the most common skill phrases so explain.py can use real
    # skill vocabulary instead of a hand-typed list
    top_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)[:800]
    with open("data/skill_vocab.json", "w", encoding="utf-8") as f:
        json.dump(top_skills, f, indent=2)

    counts = {0: 0, 1: 0, 2: 0}
    for _, _, label in pairs:
        counts[label] += 1
    print(f"wrote {len(pairs)} rows to {out_path}")
    print("class balance:", counts)
    print(f"wrote {len(top_skills)} skills to data/skill_vocab.json")


if __name__ == "__main__":
    build_dataset()
