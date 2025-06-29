# save_all_endpoints.py
import requests
import json
import sqlite3
from config.database import DB_PATH
from config.json_paths import ALL_ENDPOINTS_JSON_PATH


def fetch_all_endpoints() -> dict:
    url = "https://pokeapi.co/api/v2/"
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.json()


def save_to_json(data: dict) -> None:
    ALL_ENDPOINTS_JSON_PATH.parent.mkdir(exist_ok=True, parents=True)
    with ALL_ENDPOINTS_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 保存完了: {ALL_ENDPOINTS_JSON_PATH}")


def save_to_sqlite(data: dict, db_path, table_name: str = "endpoints"):
    db_path.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"DROP TABLE IF EXISTS {table_name}")
    c.execute(f"CREATE TABLE {table_name} (name TEXT PRIMARY KEY, url TEXT)")
    c.executemany(f"INSERT INTO {table_name} VALUES (?, ?)", data.items())
    conn.commit()
    conn.close()
    print(f"[INFO] 保存完了: {db_path}（{len(data)}件）")


if __name__ == "__main__":
    data = fetch_all_endpoints()
    save_to_sqlite(data, DB_PATH)
