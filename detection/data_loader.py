import json


class DataLoader:
    @staticmethod
    def load_data(file_path: str) -> list:
        with open(file_path) as file:
            data = json.load(file)
        traces = data["data"]
        return traces
