from pathlib import Path
import json

jsonpath = Path(__file__).parent / "raw_data" / "ability" / "00001.json"

with open(jsonpath, "r", encoding="utf-8") as f:
    data = json.load(f)

flavors = data["flavor_text_entries"]

results = []
for flavor in flavors:
    lang = flavor["language"]["name"]
    ver = flavor["version_group"]["name"]
    results.append((f"{lang} :{ver}"))

with open("flovar.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))
