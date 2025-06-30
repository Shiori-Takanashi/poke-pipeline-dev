from pathlib import Path


def dir_maker(dirpath: Path):
    dirpath.mkdir(exist_ok=True)
