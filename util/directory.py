from pathlib import Path


def dir_maker(dirpath: Path) -> None:
    dirpath.mkdir(exist_ok=True)


def json_dir_maker_from_name(name: str) -> None:
    rootpath = Path(__file__).resolve().parent.parent
    json_dirpath = rootpath / "json"
    subjson_dirpath = json_dirpath / name
    subjson_dirpath.mkdir(parents=True, exist_ok=True)
