from typing import List, Dict


def extract_idx_from_url(url: str) -> int:
    try:
        return int(url.rstrip("/").split("/")[-1])
    except (ValueError, AttributeError):
        return -1
