import json
from detection.utils import JAEGER_LOG_PATH_WITH_ERROR
from detection.data_loader import DataLoader


def detect_nplus1_queries(jaeger_data: dict) -> list:
    """
    The function `detect_nplus1_queries` analyzes Jaeger trace data to detect N+1 query issues and
    returns a list of problematic queries with their counts and corresponding trace IDs.
    
    :param jaeger_data: The `detect_nplus1_queries` function you provided is designed to detect N+1
    query issues in Jaeger trace data. It iterates through the traces in the Jaeger data, extracts
    database queries from spans, and identifies queries that are executed more than once within a single
    trace
    :type jaeger_data: dict
    :return: The `detect_nplus1_queries` function returns a list of dictionaries, where each dictionary
    represents a potential N+1 query issue detected in the Jaeger data. Each dictionary contains the
    trace ID, the query statement that was executed multiple times, and the count of how many times it
    was executed in the trace.
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
    """
    The `main` function loads Jaeger log data, detects N+1 query issues, and prints out the detected N+1
    queries with their trace IDs, queries, and counts.
    """
    jaeger_data = DataLoader(JAEGER_LOG_PATH_WITH_ERROR).get_traces()
    nplus1_issues = detect_nplus1_queries(jaeger_data)

    print("Detected N+1 Queries:")
    for issue in nplus1_issues:
        print(f"Trace ID: {issue['trace_id']}, Query: {issue['query']}, Count: {issue['count']}")


if __name__ == '__main__':
    main()
