# Resume-JD Deep Neural Network Match Scorer

A Siamese BiLSTM model that reads a resume and a job description and
classifies the pair as a Weak, Medium, or Strong match. Trained on a
real 50,000-record resume/JD dataset (`train.jsonl`), which pairs each
job description with a genuine matching resume and a slightly weakened
version of that same resume.

See `Resume_JD_Deep_Neural_Network_Concepts.docx` for the theory writeup
this project is based on.

## Project structure

```
resume_jd_dnn_project/
├── data/
│   ├── resume_jd_dataset.csv          derived dataset (resume_text, job_description, match_label)
│   └── skill_vocab.json               top 800 skill phrases pulled from the real "Skills" field
├── src/
│   ├── make_dataset.py                synthetic dataset generator (early prototype, kept for reference)
│   ├── make_dataset_real.py           builds resume_jd_dataset.csv from the real train.jsonl
│   ├── preprocessing.py               text cleaning + tokenization
│   ├── model.py                       Siamese BiLSTM architecture
│   ├── train.py                       training loop
│   ├── evaluate.py                    metrics + confusion matrix
│   ├── predict.py                     single-pair inference
│   └── explain.py                     keyword-overlap explanation
├── models/
│   ├── resume_jd_match_model.keras
│   └── tokenizer.pkl
├── outputs/
│   ├── training_history.png
│   ├── confusion_matrix.png
│   └── test_split.npz
├── Resume_JD_Deep_Neural_Network.ipynb  self-contained notebook version, runnable in Colab
└── requirements.txt
```

## Labelling logic

The raw `train.jsonl` gives each job description two resumes for the
same person:

- `Resume-matched` — the resume as originally written -> **Strong** match
- `Resume-unmatched` — a slightly weakened/edited version of the same
  resume (fewer skills listed, shortened experience) -> **Medium** match

There's no built-in negative example, so a **Weak** match is created by
pairing each JD with a `Resume-matched` pulled from a random, unrelated
record. 4,000 source records were sampled -> 12,000 labelled pairs,
evenly split across the three classes.

## Running it

```bash
pip install -r requirements.txt
cd src
python make_dataset_real.py     # rebuild data/resume_jd_dataset.csv from train.jsonl
python train.py                 # trains and saves the model + tokenizer
python evaluate.py              # prints metrics, saves confusion matrix
python predict.py               # runs one example prediction
```

Or open `Resume_JD_Deep_Neural_Network.ipynb` in Google Colab, upload
`train.jsonl` when prompted, and run all cells top to bottom.

## Results (this run)

- Test accuracy: **71.4%** (1,800 held-out pairs)
- Weak-match F1: 0.89, Medium-match F1: 0.60, Strong-match F1: 0.66
- The model separates Weak from Medium/Strong cleanly (95% precision on
  Weak). Most confusion is between Medium and Strong, which makes sense
  since those pairs come from the same underlying resume with only a
  few skills/experience lines edited out - a genuinely hard distinction.
- Full classification report and confusion matrix are in `outputs/`

## Architecture summary

Two towers (resume, JD) share one embedding layer and one BiLSTM
encoder. Each tower pools its BiLSTM output into a single vector.
The two vectors are combined via concatenation, absolute difference,
and elementwise product, then passed through two dense layers with
dropout to a 3-way softmax. Trained with Adam (lr=0.001), sparse
categorical cross-entropy, and class-weighted loss. Early stopping
(patience=5, restore best weights) kicked in around epoch 8 as the
model started overfitting the training set.
