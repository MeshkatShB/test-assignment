from detection.data_loader import DataLoader
from detection.utils import JAEGER_LOG_PATH_WITH_ERROR, TRACE_DURATION_THRESHOLD


def main():
    """
    The main function loads traces from a Jaeger log file, identifies spans with durations exceeding a
    threshold, and prints those spans.
    """
    traces = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()
    long_traces = []

    for trace in traces:
        for span in trace["spans"]:
            if span['duration'] > TRACE_DURATION_THRESHOLD:
                long_traces.append(span)

    for lt in long_traces:
        print(lt)


if __name__ == "__main__":
    main()
