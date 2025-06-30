# save_all_endpoints.py
import requests
import json
import sqlite3
from pathlib import Path
from config.anchor_config import (
    DATABASE_DIR_PATH,
    DB_FILE_PATH,
    META_DIR_PATH,
    BASE_URL,
)
from src.util.directory import dir_maker


def fetch_all_endpoints(base_url) -> dict:
    base_url = "https://pokeapi.co/api/v2/"
    res = requests.get(base_url, timeout=10)
    res.raise_for_status()
    return res.json()


def save_to_json(data: dict, dirpath: Path, file: str) -> None:
    dir_maker(dirpath)
    filepath = dirpath / file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("ENDPOINTS = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 保存完了: {filepath}")


# def save_to_sqlite(data: dict, db_path, table_name: str = "endpoints"):
#     db_path.parent.mkdir(exist_ok=True)
#     conn = sqlite3.connect(db_path)
#     c = conn.cursor()
#     c.execute(f"DROP TABLE IF EXISTS {table_name}")
#     c.execute(f"CREATE TABLE {table_name} (name TEXT PRIMARY KEY, url TEXT)")
#     c.executemany(f"INSERT INTO {table_name} VALUES (?, ?)", data.items())
#     conn.commit()
#     conn.close()
#     print(f"[INFO] 保存完了: {db_path}（{len(data)}件）")


if __name__ == "__main__":
    data = fetch_all_endpoints(BASE_URL)
    save_to_json(data, META_DIR_PATH, "endpoints.py")
