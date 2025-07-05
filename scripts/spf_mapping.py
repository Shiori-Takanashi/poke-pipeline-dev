from pathlib import Path
import json
from typing import List, Dict, Any

from config.dirpath import DEV_DIR_PATH, META_DIR_PATH, JSON_DIR_PATH
from util.io_json import read_json
from util.process_idx import extract_idx_from_url


# 定数ファイルの代わりにjsonディレクトリから直接参照
def get_json_files_mapping(subdir: str) -> Dict[str, str]:
    """指定されたサブディレクトリのJSONファイルのマッピングを取得"""
    dir_path = JSON_DIR_PATH / subdir
    if not dir_path.exists():
        return {}
    return {path.stem.zfill(5): path.name for path in dir_path.glob("*.json")}


# 実際のディレクトリパス
SPECIE_DIR_PATH = JSON_DIR_PATH / "pokemon_species"
POKEMON_DIR_PATH = JSON_DIR_PATH / "pokemon"
FORM_DIR_PATH = JSON_DIR_PATH / "pokemon_form"

# マッピング辞書を動的に作成
SPECIES = get_json_files_mapping("pokemon_species")
POKEMON = get_json_files_mapping("pokemon")
FORM = get_json_files_mapping("pokemon_form")


class MonsterMap:
    def __init__(self) -> None:
        self.map: Dict[int, Dict[str, List[int]]] = {}

    def _extract_idx_from_data(self, entries: List[Dict[str, Any]]) -> List[int]:
        ids: List[int] = []
        for entry in entries:
            if "url" in entry:
                raw = entry["url"]
            elif "pokemon" in entry and "url" in entry["pokemon"]:
                raw = entry["pokemon"]["url"]
            elif "form" in entry and "url" in entry["form"]:
                raw = entry["form"]["url"]
            else:
                continue
            ids.append(int(extract_idx_from_url(raw)))
        return ids

    def process_species(self, species_id: int) -> List[int]:
        path = SPECIES.get(str(species_id).zfill(5))
        if not path:
            return []
        data = read_json(SPECIE_DIR_PATH / path)
        return self._extract_idx_from_data(data.get("varieties", []))

    def process_pokemon(self, pokemon_ids: List[int]) -> List[int]:
        forms: List[int] = []
        for pid in pokemon_ids:
            path = POKEMON.get(str(pid).zfill(5))
            if not path:
                continue
            data = read_json(POKEMON_DIR_PATH / path)
            forms.extend(self._extract_idx_from_data(data.get("forms", [])))
        return forms

    def process_form(self, form_ids: List[int]) -> None:
        for fid in form_ids:
            if FORM.get(str(fid).zfill(5)):
                _ = FORM_DIR_PATH / FORM[str(fid).zfill(5)]

    def process_all(self, species_ids: List[int]) -> List[Dict[str, int]]:
        triples: List[Dict[str, int]] = []
        for sid in species_ids:
            pokes = self.process_species(sid)
            for pid in pokes:
                forms = self.process_pokemon([pid])
                for fid in forms:
                    triples.append({"species": sid, "pokemon": pid, "form": fid})
        return triples

    @staticmethod
    def make_spf_map(triples: List[Dict[str, int]]) -> Dict[str, Dict[str, int]]:
        # ソートを削除：triples の順序をそのまま使う
        return {f"m{(i + 1):05d}": t for i, t in enumerate(triples)}


if __name__ == "__main__":
    target_species = list(range(1, 1206))
    mm = MonsterMap()
    triples = mm.process_all(target_species)
    SPF_MAP = mm.make_spf_map(triples)

    out_path = META_DIR_PATH / "spf_map.py"
    with open(out_path, "w", encoding="utf-8") as fp:
        # 順序を気にしない：キーはアルファベット順に整列
        fp.write("SPF_MAP = ")
        fp.write(json.dumps(SPF_MAP, ensure_ascii=False, indent=2, sort_keys=True))
        fp.write("\n")
