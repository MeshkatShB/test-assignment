import unittest
from unittest.mock import patch
import numpy as np


# Mock the DataLoader and its methods
class MockDataLoader:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def get_spans():
        # Return a mock span durations array
        return [10, 20, 10, 30, 20, 10, 1000, 10, 20, 10]


# Replace the actual DataLoader with the mock
with patch('detection.data_loader.DataLoader', MockDataLoader):
    import detection.trace_classifier.anomaly_detection as ad


class TestAnomalyDetection(unittest.TestCase):
    def setUp(self):
        # Set up any state specific to the test case.
        self.span_durations = np.array([10, 20, 10, 30, 20, 10, 1000, 10, 20, 10])

    def test_isolation_forest(self):
        with patch('builtins.print') as mocked_print:
            ad.isolation_forest()
            mocked_print.assert_called()

    def test_k_means(self):
        with patch('builtins.print') as mocked_print:
            ad.k_means()
            mocked_print.assert_called()

    def test_auto_encoder(self):
        with patch('builtins.print') as mocked_print:
            ad.auto_encoder()
            mocked_print.assert_called()

    # def test_variational_auto_encoder(self):
    #     with patch('builtins.print') as mocked_print:
    #         ad.variational_auto_encoder()
    #         mocked_print.assert_called()

    def test_local_outlier_factor(self):
        with patch('builtins.print') as mocked_print:
            ad.local_outlier_factor()
            mocked_print.assert_called()


if __name__ == '__main__':
    unittest.main()
