from meta.endpoints import ENDPOINTS

from pathlib import Path

if __name__ == "__main__":
    keys = [key for key in ENDPOINTS.keys()]
    outpath = Path(__file__).parent / "out" / "endpoints.txt"
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("ALL_FETCH = [\n    ")
        f.write(",\n    ".join(f'"{key}"' for key in keys))
        f.write("\n]\n")
