"""
Runs a single resume/JD pair through the trained model and prints
a prediction, plus a simple skill-overlap explanation (see explain.py).
"""

from tensorflow.keras.models import load_model

import model  # noqa: F401  (import runs @register_keras_serializable so the custom Lambda ops can be reloaded)
from preprocessing import load_tokenizer, texts_to_padded, MAX_LEN
from explain import skill_overlap_report

MODEL_PATH = "models/resume_jd_match_model.keras"
TOKENIZER_PATH = "models/tokenizer.pkl"
CLASS_NAMES = ["Weak Match", "Medium Match", "Strong Match"]


def predict_pair(resume_text, jd_text, model=None, tokenizer=None):
    if model is None:
        model = load_model(MODEL_PATH)
    if tokenizer is None:
        tokenizer = load_tokenizer(TOKENIZER_PATH)

    resume_padded = texts_to_padded([resume_text], tokenizer, MAX_LEN)
    jd_padded = texts_to_padded([jd_text], tokenizer, MAX_LEN)

    probs = model.predict([resume_padded, jd_padded], verbose=0)[0]
    pred_class = probs.argmax()

    result = {
        "predicted_class": CLASS_NAMES[pred_class],
        "confidence": float(probs[pred_class]),
        "probabilities": {CLASS_NAMES[i]: float(p) for i, p in enumerate(probs)},
    }
    result.update(skill_overlap_report(resume_text, jd_text))
    return result


def print_result(result):
    print(f"Predicted class: {result['predicted_class']}")
    print(f"Confidence: {result['confidence']:.0%}")
    print(f"Common skills: {', '.join(result['common_skills']) or 'none found'}")
    print(f"Missing skills: {', '.join(result['missing_skills']) or 'none found'}")


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("data/resume_jd_dataset.csv")
    example = df.iloc[0]

    result = predict_pair(example["resume_text"], example["job_description"])
    print(f"(actual label: {['Weak', 'Medium', 'Strong'][example['match_label']]} Match)")
    print_result(result)
