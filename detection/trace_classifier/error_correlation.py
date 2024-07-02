import pandas as pd
from detection.data_loader import DataLoader
from detection.utils import JAEGER_LOG_PATH_WITH_ERROR


# Example for Dev time:
deployments = {
    "2024-06-29": "v1.0.0",
    "2024-06-30": "v1.1.0"
}


def main():
    """
    The main function extracts errors from Jaeger logs and correlates them with deployment versions.
    """
    traces = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()

    # Extract errors with timestamps
    errors = []
    for trace in traces:
        for span in trace["spans"]:
            if any(tag["key"] == "error" and tag["value"] is True for tag in span["tags"]):
                errors.append({"timestamp": span["startTime"], "service": span["operationName"]})

    errors_df = pd.DataFrame(errors)

    for date, version in deployments.items():
        errors_df.loc[errors_df["timestamp"] == pd.to_datetime(date).date(), "deployment"] = version

    print("Errors with Deployment Correlation:")
    print(errors_df)


if __name__ == "__main__":
    main()
