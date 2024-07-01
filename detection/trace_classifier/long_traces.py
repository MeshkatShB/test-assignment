from detection.data_loader import DataLoader

JAEGER_LOG_PATH_WITH_ERROR = '../../trace_exploration/traces/trace_generate_pairs_with_error.json'
TRACE_DURATION_THRESHOLD = 1000

traces = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()
long_traces = []

for trace in traces:
    for span in trace["spans"]:
        if span['duration'] > TRACE_DURATION_THRESHOLD:
            long_traces.append(span)

for lt in long_traces:
    print(lt)
