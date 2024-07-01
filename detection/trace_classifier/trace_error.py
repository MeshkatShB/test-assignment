import json
from detection.utils import JAEGER_LOG_PATH_WITH_ERROR
from detection.data_loader import DataLoader


data = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()


def extract_errors_warnings_exceptions(trace_data):
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
