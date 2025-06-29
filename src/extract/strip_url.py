from typing import Any, Dict, List
from src.util.io_json import read_json, write_json
from constants.pokemon_species import SPECIES
from config.paths_json import SPECIE_DIR_PATH
from config.paths_anchor import DEV_DIR_PATH
from pathlib import Path
import json
import re


def sanitize(text: str) -> str:
    # 制御文字（ASCII 0〜31）を全て空白に置換 or 削除（用途によって選択）
    # 下記はすべて削除する例（"\n", "\f", "\r", "\t" など含む）
    return re.sub(r"[\x00-\x1F]+", " ", text).strip()


def strip_url(obj, is_ancestor_varieties=False):
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():

            if k == "url" and is_ancestor_varieties:
                continue
            result[k] = strip_url(v, is_ancestor_varieties)
        return result
    elif isinstance(obj, list):
        return [strip_url(item, is_ancestor_varieties) for item in obj]
    else:
        return obj


idx = 1
idx_pad = str(idx).zfill(5)
file = SPECIES[idx_pad]
src_path = SPECIE_DIR_PATH / file

data = read_json(src_path)

debug_path = DEV_DIR_PATH / "debug.txt"
outs_path = DEV_DIR_PATH / "outs.json"

write_json(data, outs_path)
