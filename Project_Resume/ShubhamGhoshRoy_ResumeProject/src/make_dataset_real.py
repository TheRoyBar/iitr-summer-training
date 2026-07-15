"""
Converts the uploaded train.jsonl (real resume/JD data) into the same
resume_text,job_description,match_label schema the rest of the pipeline
expects, so preprocessing.py / model.py / train.py etc. don't change at all.

The raw file gives each JD two resumes for the same person:
  - Resume-matched:   the resume as originally written -> Strong match
  - Resume-unmatched: a slightly weakened/edited version of the same
                       resume (see "Filtered-information") -> Medium match

There's no built-in Weak example, so a Weak pair is created by pairing
each JD with a Resume-matched pulled from a randomly chosen, unrelated
record.
"""

import json
import random
import csv

random.seed(42)

SRC_PATH = "/mnt/user-data/uploads/train.jsonl"
OUT_PATH = "data/resume_jd_dataset.csv"
N_SAMPLE = 4000  # subset of the 50k records, keeps training time reasonable


def load_records(path, n_sample):
    records = []
    with open(path) as f:
        for line in f:
            records.append(json.loads(line))
    random.shuffle(records)
    return records[:n_sample]


def build_dataset(src_path=SRC_PATH, out_path=OUT_PATH, n_sample=N_SAMPLE):
    records = load_records(src_path, n_sample)
    rows = []

    for i, rec in enumerate(records):
        jd = rec["Job-Description"].strip()
        strong_resume = rec["Resume-matched"].strip()
        medium_resume = rec.get("Resume-unmatched", "").strip()

        rows.append((strong_resume, jd, 2))
        if medium_resume:
            rows.append((medium_resume, jd, 1))

        # weak: pair this JD with a random unrelated resume
        other = records[random.randrange(len(records))]
        while other is rec:
            other = records[random.randrange(len(records))]
        weak_resume = other["Resume-matched"].strip()
        rows.append((weak_resume, jd, 0))

    random.shuffle(rows)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["resume_text", "job_description", "match_label"])
        writer.writerows(rows)

    counts = {0: 0, 1: 0, 2: 0}
    for _, _, label in rows:
        counts[label] += 1
    print(f"wrote {len(rows)} rows to {out_path}")
    print("class balance:", counts)


if __name__ == "__main__":
    build_dataset()
