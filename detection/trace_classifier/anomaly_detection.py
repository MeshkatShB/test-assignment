import numpy as np
import pandas as pd

from detection.data_loader import DataLoader
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Dense, Lambda
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.models import Model


JAEGER_LOG_PATH_WITH_ERROR = '../../trace_exploration/traces/trace_generate_pairs_with_error.json'
span_durations = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_spans()


def isolation_forest():
    # Convert to 2D array for IsolationForest
    X = np.array(span_durations).reshape(-1, 1)

    # Fit IsolationForest model
    model = IsolationForest(contamination=0.1)
    model.fit(X)

    # Predict anomalies
    anomalies = model.predict(X)

    # Find indices of anomalies
    anomaly_indices = np.where(anomalies == -1)[0]
    anomalous_durations = [span_durations[i] for i in anomaly_indices]

    print("Anomalous Span Durations (Isolation Forest):")
    print(anomalous_durations)


def k_means():
    # Convert to 2D array
    X = np.array(span_durations).reshape(-1, 1)
    # Fit the K-Means model
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)
    distances = kmeans.transform(X).min(axis=1)

    # Set a threshold for anomaly detection
    threshold = np.percentile(distances, 90)
    anomalies = X[distances > threshold]

    print("Anomalous Span Durations (K-Means):")
    print(anomalies.flatten())


def auto_encoder():
    # Normalize the data
    X = np.array(span_durations).reshape(-1, 1).astype(float)
    X = (X - X.min()) / (X.max() - X.min())

    # Define the autoencoder model
    input_layer = Input(shape=(1,))
    encoder = Dense(8, activation="relu")(input_layer)
    encoder = Dense(4, activation="relu")(encoder)
    encoder = Dense(2, activation="relu")(encoder)
    decoder = Dense(4, activation="relu")(encoder)
    decoder = Dense(8, activation="relu")(decoder)
    decoder = Dense(1, activation="sigmoid")(decoder)
    autoencoder = Model(inputs=input_layer, outputs=decoder)

    # Compile the model
    autoencoder.compile(optimizer="adam", loss="mean_squared_error")

    # Train the model
    autoencoder.fit(X, X, epochs=100, batch_size=2, shuffle=True, validation_split=0.1, verbose=0)

    # Get the reconstruction loss
    reconstructions = autoencoder.predict(X)
    loss = np.mean(np.power(X - reconstructions, 2), axis=1)

    # Set a threshold for anomaly detection
    threshold = 0.01
    anomalies = loss > threshold

    # Create a DataFrame to display results
    results = pd.DataFrame({
        'Span Duration': span_durations,
        'Reconstruction Loss': loss,
        'Anomaly': anomalies
    })
    print(results[results['Anomaly'] == True])


def variational_auto_encoder():
    # Normalize the data
    X = np.array(span_durations).reshape(-1, 1).astype(float)
    X = (X - X.min()) / (X.max() - X.min())

    # Define the Variational Autoencoder model
    input_dim = X.shape[1]
    latent_dim = 2  # Dimensionality of the latent space

    # Encoder
    inputs = Input(shape=(input_dim,))
    h = Dense(8, activation='relu')(inputs)
    h = Dense(4, activation='relu')(h)
    z_mean = Dense(latent_dim)(h)
    z_log_var = Dense(latent_dim)(h)

    # Sampling function
    def sampling(args):
        z_mean, z_log_var = args
        epsilon = K.random_normal(shape=(K.shape(z_mean)[0], latent_dim), mean=0., stddev=1.0)
        return z_mean + K.exp(z_log_var / 2) * epsilon

    z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])

    # Decoder
    decoder_h = Dense(4, activation='relu')
    decoder_mean = Dense(input_dim, activation='sigmoid')
    h_decoded = decoder_h(z)
    x_decoded_mean = decoder_mean(h_decoded)

    # Define the VAE model
    vae = Model(inputs, x_decoded_mean)

    # VAE loss function
    reconstruction_loss = MeanSquaredError()(inputs, x_decoded_mean)
    kl_loss = -0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
    vae_loss = K.mean(reconstruction_loss + kl_loss)

    vae.add_loss(vae_loss)
    vae.compile(optimizer='adam')

    # Train the model
    vae.fit(X, X, epochs=100, batch_size=2, shuffle=True, validation_split=0.1, verbose=0)

    # Get the reconstruction loss
    reconstructions = vae.predict(X)
    loss = np.mean(np.power(X - reconstructions, 2), axis=1)

    # Set a threshold for anomaly detection
    threshold = 0.01
    anomalies = loss > threshold

    # Create a DataFrame to display results
    results = pd.DataFrame({
        'Span Duration': span_durations,
        'Reconstruction Loss': loss,
        'Anomaly': anomalies
    })

    print(results[results['Anomaly'] == True])


def local_outlier_factor():
    # Convert to 2D array
    X = np.array(span_durations).reshape(-1, 1)

    # Fit the LOF model
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
    y_pred = lof.fit_predict(X)

    # Extract anomalies
    anomalies = X[y_pred == -1]

    print("Anomalous Span Durations (LOF):")
    print(anomalies.flatten())


if __name__ == '__main__':
    isolation_forest()
    k_means()
    auto_encoder()
    variational_auto_encoder()
    local_outlier_factor()
