import unittest
from unittest.mock import patch


# Mock the DataLoader and its methods
class MockDataLoader:
    def __init__(self, path):
        self.path = path

    def get_traces(self):
        # Return mock traces with errors, warnings, and exceptions
        return [
            {
                'traceID': 'trace1',
                'spans': [
                    {
                        'spanID': 'span1',
                        'traceID': 'trace1',
                        'operationName': 'operation1',
                        'startTime': 1620000000,
                        'duration': 100,
                        'tags': [
                            {'key': 'error', 'value': True},
                            {'key': 'warning', 'value': 'Potential issue detected'}
                        ],
                        'logs': [
                            {'fields': [{'key': 'exception', 'value': 'NullPointerException'}]}
                        ]
                    }
                ]
            }
        ]


# Replace the actual DataLoader with the mock
with patch('detection.data_loader.DataLoader', MockDataLoader):
    import detection.trace_classifier.trace_error as te


class TestTraceErrorDetection(unittest.TestCase):
    def setUp(self):
        self.mock_data = [
            {
                'traceID': 'trace1',
                'spans': [
                    {
                        'spanID': 'span1',
                        'traceID': 'trace1',
                        'operationName': 'operation1',
                        'startTime': 1620000000,
                        'duration': 100,
                        'tags': [
                            {'key': 'error', 'value': True},
                            {'key': 'warning', 'value': 'Potential issue detected'}
                        ],
                        'logs': [
                            {'fields': [{'key': 'exception', 'value': 'NullPointerException'}]}
                        ]
                    }
                ]
            }
        ]
        self.expected_issues = [
            {
                'type': 'error',
                'span_id': 'span1',
                'trace_id': 'trace1',
                'operation': 'operation1',
                'start_time': 1620000000,
                'duratoin': 100,
                'message': 'Error detected in span'
            },
            {
                'type': 'warning',
                'span_id': 'span1',
                'trace_id': 'trace1',
                'operation': 'operation1',
                'start_time': 1620000000,
                'duratoin': 100,
                'message': 'Warning detected in span: Potential issue detected'
            },
            {
                'type': 'exception',
                'span_id': 'span1',
                'trace_id': 'trace1',
                'operation': 'operation1',
                'start_time': 1620000000,
                'duratoin': 100,
                'message': 'NullPointerException'
            }
        ]

    def test_extract_errors_warnings_exceptions(self):
        issues = te.extract_errors_warnings_exceptions(self.mock_data)
        self.assertEqual(issues, self.expected_issues)


if __name__ == '__main__':
    unittest.main()
