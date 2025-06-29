from pathlib import Path

BASE_URL = "https://pokeapi.co/api/v2/"
DB_NAME = "pokeinfo.db"

ROOT = Path(__file__).resolve().parent.parent

CLI_DIR_PATH = ROOT / "cli"
CONFIG_DIR_PATH = ROOT / "config"
DATABASE_DIR_PATH = ROOT / "database"
CONSTANTS_DIR_PATH = ROOT / "constants"
JSON_DIR_PATH = ROOT / "json"
MODEL_DIR_PATH = ROOT / "model"
OUT_DIR_PATH = ROOT / "out"
DEV_DIR_PATH = ROOT / "dev"
TESTS_DIR_PATH = ROOT / "tests"

DB_FILE_PATH = DATABASE_DIR_PATH / DB_NAME
