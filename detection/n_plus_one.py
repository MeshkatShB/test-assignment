import json


def load_jaeger_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def detect_nplus1_queries(jaeger_data):
    nplus1_issues = []

    for trace in jaeger_data.get('data', []):
        spans = trace.get('spans', [])
        query_counts = {}
        trace_id = trace['traceID']

        for span in spans:
            # Extract the db.statement tag from the span
            for tag in span.get('tags', []):
                if tag['key'] == 'db.statement':
                    statement = tag['value']
                    if statement not in query_counts:
                        query_counts[statement] = 0
                    query_counts[statement] += 1

        for statement, count in query_counts.items():
            if count > 1:
                nplus1_issues.append({
                    'trace_id': trace_id,
                    'query': statement,
                    'count': count
                })

    return nplus1_issues


def main():
    file_path = '../trace_exploration/traces/trace_generate_pairs_with_error.json'
    jaeger_data = load_jaeger_data(file_path)
    nplus1_issues = detect_nplus1_queries(jaeger_data)

    print("Detected N+1 Queries:")
    for issue in nplus1_issues:
        print(f"Trace ID: {issue['trace_id']}, Query: {issue['query']}, Count: {issue['count']}")


if __name__ == '__main__':
    main()
