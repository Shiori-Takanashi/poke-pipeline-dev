import json
from typing import List, Dict


def read_json(json_full_path) -> List | Dict:
    with open(json_full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(json_data, out_full_path) -> None:
    with open(out_full_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
