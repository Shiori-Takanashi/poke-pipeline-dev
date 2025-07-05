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
