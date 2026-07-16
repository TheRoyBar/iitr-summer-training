"""
Trains the Siamese BiLSTM model on the resume/JD dataset and saves
the model + tokenizer + training history plot.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from preprocessing import prepare_dataset, save_tokenizer, MAX_LEN, VOCAB_SIZE
from model import build_model

DATA_PATH = "data/resume_jd_dataset.csv"
MODEL_PATH = "models/resume_jd_match_model.keras"
TOKENIZER_PATH = "models/tokenizer.pkl"
HISTORY_PLOT_PATH = "outputs/training_history.png"


def load_data(path=DATA_PATH):
    return pd.read_csv(path)


def split_data(resume_padded, jd_padded, labels, test_size=0.15, val_size=0.15, seed=42):
    # first split off test set, then split remaining into train/val
    r_temp, r_test, j_temp, j_test, y_temp, y_test = train_test_split(
        resume_padded, jd_padded, labels, test_size=test_size, stratify=labels, random_state=seed
    )
    val_fraction = val_size / (1 - test_size)
    r_train, r_val, j_train, j_val, y_train, y_val = train_test_split(
        r_temp, j_temp, y_temp, test_size=val_fraction, stratify=y_temp, random_state=seed
    )
    return (r_train, j_train, y_train), (r_val, j_val, y_val), (r_test, j_test, y_test)


def plot_history(history, path=HISTORY_PLOT_PATH):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].plot(history.history["loss"], label="train loss")
    axes[0].plot(history.history["val_loss"], label="val loss")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("epoch")
    axes[0].legend()

    axes[1].plot(history.history["accuracy"], label="train acc")
    axes[1].plot(history.history["val_accuracy"], label="val acc")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("epoch")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(path)
    print(f"saved training history plot to {path}")


def main(epochs=12, batch_size=64):
    df = load_data()
    resume_padded, jd_padded, labels, tokenizer = prepare_dataset(df, max_len=MAX_LEN, vocab_size=VOCAB_SIZE)
    save_tokenizer(tokenizer, TOKENIZER_PATH)

    train, val, test = split_data(resume_padded, jd_padded, labels)
    r_train, j_train, y_train = train
    r_val, j_val, y_val = val
    r_test, j_test, y_test = test

    vocab_size = min(VOCAB_SIZE, len(tokenizer.word_index) + 1)
    model = build_model(vocab_size=vocab_size, max_len=MAX_LEN)
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])

    early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

    # weak/medium/strong are not perfectly balanced, so weight classes
    # to stop the model from just ignoring the minority (weak) class
    class_weights_arr = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
    class_weight = {i: w for i, w in enumerate(class_weights_arr)}

    history = model.fit(
        [r_train, j_train], y_train,
        validation_data=([r_val, j_val], y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stop],
        class_weight=class_weight,
        verbose=2,
    )

    plot_history(history)
    model.save(MODEL_PATH)
    print(f"saved model to {MODEL_PATH}")

    test_loss, test_acc = model.evaluate([r_test, j_test], y_test, verbose=0)
    print(f"test loss: {test_loss:.4f}, test accuracy: {test_acc:.4f}")

    # keep test split around on disk so evaluate.py can reuse the exact same split
    np.savez("outputs/test_split.npz", r_test=r_test, j_test=j_test, y_test=y_test)

    return model, tokenizer, (r_test, j_test, y_test)


if __name__ == "__main__":
    main()
