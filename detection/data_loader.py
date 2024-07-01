import json


class DataLoader:
    def __init__(self, file_path: str) -> None:
        self.traces = None
        self.file_path = file_path
        self._load_data()

    def _load_data(self) -> None:
        with open(self.file_path) as file:
            data = json.load(file)
        traces = data["data"]
        self.traces = traces

    def get_spans(self) -> list:
        return [span["duration"] for trace in self.traces for span in trace["spans"]]

    def get_traces(self):
        return self.traces
