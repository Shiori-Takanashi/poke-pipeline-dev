# save_target_endpoints.py
import sqlite3
from config.paths_db import DB_PATH
from constants.targets import FETCH_TARGET


def create_target_table(
    db_path, source_table="endpoints", target_table="target_endpoints"
):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(f"DROP TABLE IF EXISTS {target_table}")
    c.execute(f"CREATE TABLE {target_table} (name TEXT PRIMARY KEY, url TEXT)")

    placeholders = ",".join("?" for _ in FETCH_TARGET)
    query = f"SELECT name, url FROM {source_table} WHERE name IN ({placeholders})"
    c.execute(query, FETCH_TARGET)
    rows = c.fetchall()

    c.executemany(f"INSERT INTO {target_table} VALUES (?, ?)", rows)
    conn.commit()
    conn.close()
    print(f"[INFO] target_endpoints に {len(rows)} 件を保存しました")


if __name__ == "__main__":
    create_target_table(DB_PATH)
