"""
Text cleaning + tokenization utilities for the resume/JD dataset.

Both resume text and JD text are passed through the same cleaning
function and the same tokenizer, since the Siamese towers share
weights and need the two inputs represented in the same vocabulary
space.
"""

import re
import pickle

import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_LEN = 140          # tokens per document, resumes/JDs get truncated or padded to this
VOCAB_SIZE = 15000      # cap on tokenizer vocabulary


def clean_text(text):
    """lowercase, strip punctuation, collapse whitespace"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fit_tokenizer(resume_texts, jd_texts, vocab_size=VOCAB_SIZE):
    """
    fits one shared tokenizer over resumes + JDs combined, since both
    towers use the same embedding table (shared weights)
    """
    cleaned = [clean_text(t) for t in list(resume_texts) + list(jd_texts)]
    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(cleaned)
    return tokenizer


def texts_to_padded(texts, tokenizer, max_len=MAX_LEN):
    cleaned = [clean_text(t) for t in texts]
    sequences = tokenizer.texts_to_sequences(cleaned)
    padded = pad_sequences(sequences, maxlen=max_len, padding="post", truncating="post")
    return padded


def save_tokenizer(tokenizer, path="models/tokenizer.pkl"):
    with open(path, "wb") as f:
        pickle.dump(tokenizer, f)


def load_tokenizer(path="models/tokenizer.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)


def prepare_dataset(df, tokenizer=None, max_len=MAX_LEN, vocab_size=VOCAB_SIZE):
    """
    takes the raw dataframe (resume_text, job_description, match_label)
    and returns padded integer arrays ready to feed into the model,
    fitting a new tokenizer if one isn't passed in
    """
    if tokenizer is None:
        tokenizer = fit_tokenizer(df["resume_text"], df["job_description"], vocab_size)

    resume_padded = texts_to_padded(df["resume_text"], tokenizer, max_len)
    jd_padded = texts_to_padded(df["job_description"], tokenizer, max_len)
    labels = np.array(df["match_label"])

    return resume_padded, jd_padded, labels, tokenizer
