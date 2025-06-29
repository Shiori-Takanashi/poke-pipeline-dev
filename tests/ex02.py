from models import Model
import json

with open("00001.json", encoding="utf-8") as f:
    data = json.load(f)

ability = Model.model_validate(data)

# ポケモン一覧を出力
for item in ability.pokemon:
    name = item.pokemon.name
    url = item.pokemon.url
    idx = url.rstrip("/").split("/")[-1]
    slot = item.slot
    print(f"{name=}, {idx=}, {slot=}")
