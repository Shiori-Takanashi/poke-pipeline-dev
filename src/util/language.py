# util/language.py
def is_ja(entry: dict) -> bool:
    return entry.get("language", {}).get("name") == "ja"
