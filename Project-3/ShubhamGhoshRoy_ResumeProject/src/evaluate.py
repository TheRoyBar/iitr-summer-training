"""
Loads the trained model and the held-out test split, then reports
precision/recall/F1 and a confusion matrix plot.
"""

import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix

import model  # noqa: F401  (import runs @register_keras_serializable so the custom Lambda ops can be reloaded)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MODEL_PATH = "models/resume_jd_match_model.keras"
TEST_SPLIT_PATH = "outputs/test_split.npz"
CONF_MATRIX_PATH = "outputs/confusion_matrix.png"
CLASS_NAMES = ["Weak", "Medium", "Strong"]


def plot_confusion_matrix(cm, path=CONF_MATRIX_PATH):
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")

    ax.set_xticks(range(len(CLASS_NAMES)))
    ax.set_yticks(range(len(CLASS_NAMES)))
    ax.set_xticklabels(CLASS_NAMES)
    ax.set_yticklabels(CLASS_NAMES)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                     color="white" if cm[i, j] > cm.max() / 2 else "black")

    fig.colorbar(im)
    fig.tight_layout()
    fig.savefig(path)
    print(f"saved confusion matrix plot to {path}")


def main():
    model = load_model(MODEL_PATH)
    data = np.load(TEST_SPLIT_PATH)
    r_test, j_test, y_test = data["r_test"], data["j_test"], data["y_test"]

    probs = model.predict([r_test, j_test], verbose=0)
    preds = np.argmax(probs, axis=1)

    print(classification_report(y_test, preds, target_names=CLASS_NAMES))

    cm = confusion_matrix(y_test, preds)
    print("confusion matrix:")
    print(cm)
    plot_confusion_matrix(cm)


if __name__ == "__main__":
    main()
