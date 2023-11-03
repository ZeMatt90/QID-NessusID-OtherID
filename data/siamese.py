import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

class SiameseModel:
    def __init__(self, input_dim):
        self.input_dim = input_dim
        self.model = self.build_model()

    def build_model(self):
        input_a = keras.Input(shape=(self.input_dim,))
        input_b = keras.Input(shape=(self.input_dim,))

        shared_model = keras.Sequential([
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
        ])

        output_a = shared_model(input_a)
        output_b = shared_model(input_b)

        # Calcola la distanza euclidea tra le uscite
        distance = keras.layers.Lambda(lambda x: tf.norm(x[0] - x[1], axis=1)(outputs))

        model = keras.Model(inputs=[input_a, input_b], outputs=distance)
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        return model

    def train(self, X_train, y_train, epochs=10, batch_size=32):
        self.model.fit([X_train[:, 0], X_train[:, 1]], y_train, epochs=epochs, batch_size=batch_size)

    def predict(self, X_test):
        return self.model.predict([X_test[:, 0], X_test[:, 1]])

# Esempio di utilizzo:
# Definisci i dati di addestramento X_train e le etichette y_train
# Si supponga che X_train sia una matrice con due colonne, una per ciascun input
# y_train contiene le etichette corrispondenti alla similarità tra le coppie
# dei punti X_train

# input_dim è la dimensione dell'input, ovvero il numero di colonne in X_train
input_dim = X_train.shape[1]

siamese_model = SiameseModel(input_dim)
siamese_model.train(X_train, y_train, epochs=10, batch_size=32)

# Ora puoi utilizzare siamese_model per calcolare la similarità tra le righe
similarity_scores = siamese_model.predict(X_test)
