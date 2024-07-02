import json
from detection.utils import JAEGER_LOG_PATH_WITH_ERROR
from detection.data_loader import DataLoader


data = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()


def extract_errors_warnings_exceptions(trace_data):
    """
    The function `extract_errors_warnings_exceptions` parses trace data to extract errors, warnings, and
    exceptions along with relevant information.
    
    :param trace_data: Trace data is a collection of spans that represent the execution of operations
    within a distributed system. Each span contains information such as span ID, trace ID, operation
    name, tags, logs, start time, and duration. The function `extract_errors_warnings_exceptions`
    iterates through the trace data to identify and
    :return: The function `extract_errors_warnings_exceptions` returns a list of dictionaries, where
    each dictionary represents an issue found in the trace data. The dictionaries contain information
    about the type of issue (error, warning, or exception), the span ID, trace ID, operation name, start
    time, duration, and a message describing the issue.
    """
    issues = []

    for trace in trace_data :
        for span in trace['spans']:
            span_id = span['spanID']
            trace_id = span['traceID']
            operation = span['operationName']

            # Check for error or warning tags
            for tag in span['tags']:
                if tag['key'] == 'error' and tag['value'] is True:
                    issues.append({
                        'type': 'error',
                        'span_id': span_id,
                        'trace_id': trace_id,
                        'operation': operation,
                        'start_time': span['startTime'],
                        'duratoin': span['duration'],
                        'message': 'Error detected in span'
                    })
                elif 'warning' in tag['key'] or 'otel.status_code' in tag['key']:
                    issues.append({
                        'type': 'warning',
                        'span_id': span_id,
                        'trace_id': trace_id,
                        'operation': operation,
                        'start_time': span['startTime'],
                        'duratoin': span['duration'],
                        'message': f"Warning detected in span: {tag['value']}"
                    })

            # Check logs for exceptions
            for log in span['logs']:
                for field in log['fields']:
                    if 'exception' in field['key']:
                        issues.append({
                            'type': 'exception',
                            'span_id': span_id,
                            'trace_id': trace_id,
                            'operation': operation,
                            'start_time': span['startTime'],
                            'duratoin': span['duration'],
                            'message': field['value']
                        })

    return issues


if __name__ == "__main__":
    issues = extract_errors_warnings_exceptions(data)
    print("Detected Issues:", json.dumps(issues, indent=2))
