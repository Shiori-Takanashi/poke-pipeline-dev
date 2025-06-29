from __future__ import annotations
from pathlib import Path

import json
from typing import Dict, List
from .paths_anchor import JSON_DIR_PATH
from constants.targets import FETCH_TARGET, MONSTER_TARGET

SPECIE_DIR_PATH = JSON_DIR_PATH / "pokemon-species"
POKEMON_DIR_PATH = JSON_DIR_PATH / "pokemon"
FORM_DIR_PATH = JSON_DIR_PATH / "pokemon-form"
MONSTER_DIR_PATHS = [SPECIE_DIR_PATH, POKEMON_DIR_PATH, FORM_DIR_PATH]

FMT_SPECIES_DIR_PATH = JSON_DIR_PATH / "fmt-pokemon-species"
FMT_POKEMON_DIR_PATH = JSON_DIR_PATH / "fmt-pokemon"
FMT_FORM_DIR_PATH = JSON_DIR_PATH / "fmt-pokemon-form"
FMT_MONSTER_DIR_PATHS = [FMT_SPECIES_DIR_PATH, FMT_POKEMON_DIR_PATH, FMT_FORM_DIR_PATH]
