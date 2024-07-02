import unittest
from unittest.mock import patch


# Mock the DataLoader and its methods
class MockDataLoader:
    def __init__(self, path):
        self.path = path

    def get_traces(self):
        # Return mock traces with N+1 query issues
        return [
            {
                'traceID': 'trace1',
                'spans': [
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM users'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM users'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM orders'}]
                    }
                ]
            },
            {
                'traceID': 'trace2',
                'spans': [
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM products'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM products'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM products'}]
                    }
                ]
            }
        ]


# Replace the actual DataLoader with the mock
with patch('detection.data_loader.DataLoader', MockDataLoader):
    import detection.trace_classifier.n_plus_one as np1


class TestNPlusOneDetection(unittest.TestCase):
    def setUp(self):
        self.mock_data = [
            {
                'traceID': 'trace1',
                'spans': [
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM users'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM users'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM orders'}]
                    }
                ]
            },
            {
                'traceID': 'trace2',
                'spans': [
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM products'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM products'}]
                    },
                    {
                        'tags': [{'key': 'db.statement', 'value': 'SELECT * FROM products'}]
                    }
                ]
            }
        ]
        self.expected_issues = [
            {'trace_id': 'trace1', 'query': 'SELECT * FROM users', 'count': 2},
            {'trace_id': 'trace2', 'query': 'SELECT * FROM products', 'count': 3}
        ]

    def test_detect_nplus1_queries(self):
        issues = np1.detect_nplus1_queries(self.mock_data)
        self.assertEqual(issues, self.expected_issues)

    def test_main(self):
        with patch('builtins.print') as mocked_print:
            np1.main()
            # Verify that print was called with the expected output
            mocked_print.assert_any_call("Detected N+1 Queries:")
            for issue in self.expected_issues:
                mocked_print.assert_any_call(f"Trace ID: {issue['trace_id']}, Query: {issue['query']}, Count: {issue['count']}")


if __name__ == '__main__':
    unittest.main()
