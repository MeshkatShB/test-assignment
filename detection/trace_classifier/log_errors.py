import re
from detection.data_loader import DataLoader

JAEGER_LOG_PATH_WITH_ERROR = '../../trace_exploration/traces/trace_generate_pairs_with_error.json'


traces = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()

error_pattern = re.compile(r"error", re.IGNORECASE)
errors = []
long_traces = []

for trace in traces:
    for span in trace["spans"]:
        for tag in span["tags"]:
            if tag["key"] == "error" and tag["value"] is True:
                errors.append(span)

print("Errors found:")
for error in errors:
    print(error)
