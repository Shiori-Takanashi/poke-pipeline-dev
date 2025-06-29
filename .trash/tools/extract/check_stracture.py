from models import Model
import json
from pathlib import Path

json_dir = Path("raw_data/ability/")
count = 0
for path in json_dir.glob("*.json"):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        Model.model_validate(data)
        count += 1
    except Exception as e:
        print(f"エラー: {path.name} → {e}")

print(f"{count} is all OK.")
