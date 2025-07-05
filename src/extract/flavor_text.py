from pathlib import Path
from typing import Dict, List
import json

from config.json_paths import SAMPLE_DIR_PATH, CHECK_DIR_PATH
from cli.util.language import is_ja
from cli.util.version import extract_version_id
from cli.util.io import write_json
from cli.util.logger import get_logger


def latest_flavor_text(entries: List[Dict]) -> Dict[str, str]:
    result, latest = {}, -1
    for e in entries:
        if not is_ja(e):
            continue
        v_id = extract_version_id(e.get("version", {}).get("url", ""))
        if v_id > latest:
            latest = v_id
            result["flavor_text"] = e.get("flavor_text", "")
    return result


def main() -> None:
    sample = SAMPLE_DIR_PATH / "00001.json"
    prefix = "s_"

    with sample.open(encoding="utf-8") as f:
        data = json.load(f)

    out = latest_flavor_text(data.get("flavor_text_entries", []))
    dst = CHECK_DIR_PATH / f"{prefix}ft_00001.json"
    write_json(out, dst)
    logger.info(f"{dst.name} 書き込み成功")


if __name__ == "__main__":
    main()
