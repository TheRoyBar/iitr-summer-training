"""
Builds the synthetic resume - job description dataset used for training.

I generate synthetic data instead of scraping real resumes because
real resume/JD pairs are hard to get labelled with a match score,
and for a course project the goal is to show the model architecture
works, not to build a production-grade labelled corpus.

Each row is one (resume, job_description, match_label) triple.
match_label: 0 = Weak, 1 = Medium, 2 = Strong
"""

import csv
import random

random.seed(42)

# skill pools grouped by role family. a resume/JD pulls skills mainly
# from one family, which is what creates the weak/medium/strong signal
ROLE_SKILLS = {
    "ai_ml": ["Python", "TensorFlow", "PyTorch", "scikit-learn", "pandas",
              "NumPy", "deep learning", "NLP", "computer vision", "LSTM",
              "transformers", "MLOps", "model deployment", "feature engineering"],
    "backend": ["Python", "Java", "Spring Boot", "REST APIs", "FastAPI",
                "PostgreSQL", "Docker", "Kubernetes", "microservices",
                "Redis", "message queues", "system design"],
    "frontend": ["JavaScript", "React", "TypeScript", "CSS", "HTML",
                 "Redux", "Next.js", "Tailwind", "responsive design",
                 "Webpack", "accessibility"],
    "data_eng": ["SQL", "Spark", "Airflow", "ETL pipelines", "Kafka",
                 "data warehousing", "Python", "AWS", "BigQuery",
                 "data modeling", "dbt"],
    "genai": ["RAG pipelines", "vector databases", "prompt engineering",
              "LangChain", "LLM fine-tuning", "embeddings", "semantic search",
              "Python", "OpenAI API", "agentic workflows"],
}

ROLE_TITLES = {
    "ai_ml": ["Machine Learning Engineer", "AI Engineer", "Data Scientist"],
    "backend": ["Backend Developer", "Software Engineer", "Backend Engineer"],
    "frontend": ["Frontend Developer", "UI Engineer", "React Developer"],
    "data_eng": ["Data Engineer", "Analytics Engineer", "ETL Developer"],
    "genai": ["GenAI Engineer", "LLM Engineer", "AI Applications Engineer"],
}

RESUME_TEMPLATES = [
    "{name} is a {level} professional with experience in {skills}. "
    "Worked on projects involving {proj_skill} and delivered measurable results. "
    "Familiar with {extra_skill} and comfortable working in agile teams.",

    "Experienced {level} candidate skilled in {skills}. Built and shipped "
    "features using {proj_skill}. Has hands-on exposure to {extra_skill} "
    "through internships and personal projects.",

    "{name} has a background in {skills}, with recent work centered on "
    "{proj_skill}. Also explored {extra_skill} during coursework and "
    "hackathons, and enjoys solving practical engineering problems.",
]

JD_TEMPLATES = [
    "We are hiring a {title} with strong skills in {skills}. The ideal "
    "candidate should have hands-on experience with {proj_skill} and be "
    "comfortable learning {extra_skill}.",

    "Looking for a {title} to join our team. Required skills: {skills}. "
    "Experience with {proj_skill} is a must. Exposure to {extra_skill} "
    "is a plus.",

    "Open role: {title}. You will work primarily with {skills} and "
    "{proj_skill} on a daily basis. Bonus if you know {extra_skill}.",
]

NAMES = ["The candidate", "This applicant", "The resume owner"]
LEVELS = ["junior", "mid-level", "senior"]


def pick_skills(family, k):
    pool = ROLE_SKILLS[family]
    return random.sample(pool, k=min(k, len(pool)))


def make_resume(family, level):
    skills = pick_skills(family, 4)
    proj_skill = random.choice(skills)
    extra_skill = random.choice(ROLE_SKILLS[family])
    template = random.choice(RESUME_TEMPLATES)
    return template.format(
        name=random.choice(NAMES),
        level=level,
        skills=", ".join(skills),
        proj_skill=proj_skill,
        extra_skill=extra_skill,
    )


def make_jd(family):
    skills = pick_skills(family, 4)
    proj_skill = random.choice(skills)
    extra_skill = random.choice(ROLE_SKILLS[family])
    title = random.choice(ROLE_TITLES[family])
    template = random.choice(JD_TEMPLATES)
    return template.format(
        title=title,
        skills=", ".join(skills),
        proj_skill=proj_skill,
        extra_skill=extra_skill,
    )


def make_row():
    """
    Strong  -> resume and JD drawn from the same role family
    Medium  -> same family but resume is junior-level / JD wants senior,
               or the families are adjacent (ai_ml <-> genai, backend <-> data_eng)
    Weak    -> resume and JD drawn from unrelated families
    """
    families = list(ROLE_SKILLS.keys())
    adjacent = {"ai_ml": "genai", "genai": "ai_ml", "backend": "data_eng", "data_eng": "backend"}

    r = random.random()
    if r < 0.4:
        # strong match: same family
        family = random.choice(families)
        resume = make_resume(family, random.choice(LEVELS))
        jd = make_jd(family)
        label = 2
    elif r < 0.75:
        # medium match: adjacent family, or same family different seniority framing
        family = random.choice(families)
        if family in adjacent and random.random() < 0.5:
            resume_family = family
            jd_family = adjacent[family]
        else:
            resume_family = jd_family = family
        resume = make_resume(resume_family, "junior")
        jd = make_jd(jd_family)
        label = 1
    else:
        # weak match: unrelated families
        family_a, family_b = random.sample(families, 2)
        resume = make_resume(family_a, random.choice(LEVELS))
        jd = make_jd(family_b)
        label = 0

    return resume, jd, label


def build_dataset(n_rows=2000, out_path="data/resume_jd_dataset.csv"):
    rows = [make_row() for _ in range(n_rows)]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["resume_text", "job_description", "match_label"])
        writer.writerows(rows)
    print(f"wrote {n_rows} rows to {out_path}")
    counts = {0: 0, 1: 0, 2: 0}
    for _, _, label in rows:
        counts[label] += 1
    print("class balance:", counts)


if __name__ == "__main__":
    build_dataset()
