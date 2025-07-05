from typing import List, Dict, Any
from util.logger import get_logger

logger = get_logger("check_species")


def is_top_obj(obj: Any) -> bool:
    if isinstance(obj, dict):
        True
    else:
        logger.error("Json Response is invalid.")


def get_all_keys(obj: dict) -> bool:
    keys = sorted(list(obj.keys()))
    results = [defkey == key for defkey, key in zip(defkeys, keys)]
    if all(results):
        True
    else:
        logger.error("Top keys is invalid.")
