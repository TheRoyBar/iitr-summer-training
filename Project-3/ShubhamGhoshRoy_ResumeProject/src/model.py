"""
Siamese BiLSTM model for resume-JD match classification.

Two towers (resume, JD) share the same embedding + BiLSTM encoder.
The encoded vectors are combined with concatenation, absolute
difference, and element-wise product before going through dense
layers to a 3-way softmax (weak / medium / strong).
"""

import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.saving import register_keras_serializable


# named functions instead of python lambdas so the model can be saved
# and reloaded safely (Keras 3 blocks deserializing raw lambda functions)
@register_keras_serializable()
def abs_difference(tensors):
    u, v = tensors
    return tf.abs(u - v)


@register_keras_serializable()
def elementwise_product(tensors):
    u, v = tensors
    return u * v


def build_model(vocab_size, max_len, embed_dim=64, lstm_units=48,
                 dense_units=(128, 64), num_classes=3, dropout_rate=0.3):

    resume_input = layers.Input(shape=(max_len,), name="resume_input")
    jd_input = layers.Input(shape=(max_len,), name="jd_input")

    # shared layers - same weights used for both towers, this is what
    # makes it a Siamese network rather than two independent encoders
    embedding = layers.Embedding(vocab_size, embed_dim, mask_zero=True, name="shared_embedding")
    bilstm = layers.Bidirectional(layers.LSTM(lstm_units, return_sequences=True), name="shared_bilstm")
    pool = layers.GlobalMaxPooling1D(name="shared_pool")

    def encode(x):
        x = embedding(x)
        x = bilstm(x)
        x = pool(x)
        return x

    u = encode(resume_input)
    v = encode(jd_input)

    diff = layers.Lambda(abs_difference, name="abs_diff")([u, v])
    prod = layers.Lambda(elementwise_product, name="elementwise_product_layer")([u, v])

    features = layers.Concatenate(name="comparison_features")([u, v, diff, prod])

    x = features
    for units in dense_units:
        x = layers.Dense(units, activation="relu")(x)
        x = layers.Dropout(dropout_rate)(x)

    output = layers.Dense(num_classes, activation="softmax", name="match_class")(x)

    model = Model(inputs=[resume_input, jd_input], outputs=output, name="siamese_bilstm_resume_jd")
    return model


if __name__ == "__main__":
    m = build_model(vocab_size=5000, max_len=40)
    m.summary()
