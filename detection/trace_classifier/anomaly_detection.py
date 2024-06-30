import numpy as np
from detection.data_loader import DataLoader
from sklearn.ensemble import IsolationForest

JAEGER_LOG_PATH_WITH_ERROR = '../../trace_exploration/traces/trace_generate_pairs_with_error.json'


traces = DataLoader.load_data(JAEGER_LOG_PATH_WITH_ERROR)

# Collect durations of all spans
span_durations = [span["duration"] for trace in traces for span in trace["spans"]]

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

print("Anomalous Span Durations:")
print(anomalous_durations)
