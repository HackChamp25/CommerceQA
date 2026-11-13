import json

from pathlib import Path

def load_test_data(file_name: str):
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "test_data" / file_name
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data