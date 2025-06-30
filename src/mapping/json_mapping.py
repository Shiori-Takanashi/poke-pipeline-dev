# src/build/json_path_exporter.py

from pathlib import Path
import json

from config.paths_json import SPECIE_DIR_PATH, POKEMON_DIR_PATH, FORM_DIR_PATH
from config.paths_anchor import CONSTANTS_DIR_PATH


class JsonPathExporter:
    def __init__(self, output_subdir: str | None = None):
        if output_subdir:
            self.output_dir = CONSTANTS_DIR_PATH / output_subdir
            self.output_dir.mkdir(exist_ok=True)
        else:
            self.output_dir = CONSTANTS_DIR_PATH  # 直下に出力

    def make_path_index(self, dir_path: Path) -> dict[str, str]:
        return {path.stem: path.name for path in dir_path.glob("*.json")}

    def write_index_to_file(self, data: dict, label: str) -> None:
        const_name = "_".join(part.upper() for part in label.split("-"))
        output_path = self.output_dir / f"{label}.py"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"{const_name} = ")
            json.dump(data, f, indent=4, ensure_ascii=False)

    def process(self, dir_paths: list[Path]) -> None:
        for dir_path in dir_paths:
            path_index = self.make_path_index(dir_path)
            self.write_index_to_file(path_index, dir_path.name)
