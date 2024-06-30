import pandas as pd
from detection.data_loader import DataLoader
import time


# Sample deployment events
deployments = {
    "2024-06-29": "v1.0.0",
    "2024-06-30": "v1.1.0"
}

JAEGER_LOG_PATH_WITH_ERROR = '../../trace_exploration/traces/trace_generate_pairs_with_error.json'

traces = DataLoader.load_data(JAEGER_LOG_PATH_WITH_ERROR)

# Extract errors with timestamps
errors = []
for trace in traces:
    for span in trace["spans"]:
        if any(tag["key"] == "error" and tag["value"] is True for tag in span["tags"]):
            errors.append({"timestamp": span["startTime"], "service": span["operationName"]})


# Create a DataFrame
errors_df = pd.DataFrame(errors)

# Add deployment events to DataFrame
for date, version in deployments.items():
    errors_df.loc[errors_df["timestamp"] == pd.to_datetime(date).date(), "deployment"] = version

print("Errors with Deployment Correlation:")
print(errors_df)
