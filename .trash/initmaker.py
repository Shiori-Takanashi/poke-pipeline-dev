from __future__ import annotations
from pathlib import Path
from typing import List
import logging

logging.basicConfig(level=logging.INFO)


def get_child_dirs(root: Path) -> List[Path]:
    ds: List[Path] = []
    for d in root.iterdir():
        if d.is_dir():
            ds.append(d)
    return ds


def process(dirspaths: List[Path]) -> int:
    count = 0
    for dirpath in dirspaths:
        flag: bool = search(dirpath)
        if flag:
            make_init(dirpath)
            count += 1
    return count


def search(dirpath: Path) -> bool:
    for _ in dirpath.glob("*.py"):
        return True
    return False


def make_init(dirpath: Path) -> None:
    fp = dirpath / "__init__.py"
    try:
        with open(fp, "w", encoding="utf-8") as f:
            f.write("# This init file was made by a script!")
    except Exception as e:
        logging.error(f"At {fp} : {e}")


def main() -> None:
    root: Path = Path(__file__).resolve().parent.parent
    ds: List[Path] = get_child_dirs(root)
    count = process(ds)
    logging.info(f"{count} __init__.py files were created under {root}.")
