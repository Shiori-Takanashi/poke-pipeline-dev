import requests
import json
from config.network import API_ROOT


def test(keyword: str, ident: str) -> None:
    url = API_ROOT + keyword + "/488"
    res = requests.get(url)
    data = res.json()
    with open(f"dev/{ident}488.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


test("/pokemon", "p")
test("/pokemon-species", "s")
test("/pokemon-form", "f")
