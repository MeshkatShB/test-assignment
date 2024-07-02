import json
from detection.utils import JAEGER_LOG_PATH_WITH_ERROR
from detection.data_loader import DataLoader


def detect_nplus1_queries(jaeger_data: dict) -> list:
    """
    Detect N+1 queries in Jaeger trace data.

    This function analyzes the Jaeger trace data to identify instances of N+1 queries, where
    multiple database statements are executed as a single query. The function returns a list
    of dictionaries, each representing an N+1 query issue with the following fields:
        - `trace_id`: The ID of the trace containing the N+1 query.
        - `query`: The SQL statement or query that was executed multiple times.
        - `count`: The number of times the query was executed.

    Args:
        jaeger_data (dict): Jaeger trace data in JSON format.

    Returns:
        list: A list of dictionaries representing N+1 query issues found in the trace data.
    """
    nplus1_issues = []

    for trace in jaeger_data:
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
    jaeger_data = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()
    nplus1_issues = detect_nplus1_queries(jaeger_data)

    print("Detected N+1 Queries:")
    for issue in nplus1_issues:
        print(f"Trace ID: {issue['trace_id']}, Query: {issue['query']}, Count: {issue['count']}")


if __name__ == '__main__':
    main()