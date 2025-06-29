from typing import Any, Dict, List
from src.util.io_json import read_json, write_json
from constants.pokemon_species import SPECIES
from config.paths_json import SPECIE_DIR_PATH
from config.paths_anchor import DEV_DIR_PATH
from pathlib import Path


def strip_url_except_in_varieties(obj, under_varieties=False):
    if isinstance(obj, dict):
        cleaned = {}
        for key, value in obj.items():
            # varieties の下に入ったらフラグを True にして以降に伝播
            is_under_varieties = under_varieties or (key == "varieties")

            # "url" キーを削除する条件：祖先に "varieties" を含まない場合のみ
            if key == "url" and not is_under_varieties:
                continue

            cleaned[key] = strip_url_except_in_varieties(value, is_under_varieties)
        return cleaned

    elif isinstance(obj, list):
        return [strip_url_except_in_varieties(item, under_varieties) for item in obj]

    else:
        return obj


def collapse_name(obj):
    """ """
    if isinstance(obj, dict):
        # 最小辞書かどうか判定
        if set(obj.keys()) == {"name"}:
            return obj["name"]
        return {k: collapse_name(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [collapse_name(item) for item in obj]
    return obj


def unwrap_single_dict_list(obj):
    """
    リスト内に単一のネストされていない辞書しかない場合、
    [ { ... } ] → { ... } にアンラップする。
    それ以外は再帰的に走査してそのまま返す。
    """
    # 辞書ならキーごとに再帰
    if isinstance(obj, dict):
        return {k: unwrap_single_dict_list(v) for k, v in obj.items()}

    # リストなら要素をチェック
    if isinstance(obj, list):
        # 「長さ1」「要素がdict」「そのdict内にdict/listを含まない」ならアンラップ
        if (
            len(obj) == 1
            and isinstance(obj[0], dict)
            and all(not isinstance(v, (dict, list)) for v in obj[0].values())
        ):
            # dict自身も再帰処理
            return unwrap_single_dict_list(obj[0])
        # それ以外は各要素を再帰処理したリストを返す
        return [unwrap_single_dict_list(item) for item in obj]

    # その他（プリミティブ値など）はそのまま
    return obj


def filter_by_language(obj, allowed=("ja", "ja-Hrkt")):
    """
    ・obj が dict の場合：値を再帰的に処理
    ・obj が list の場合：
        - 各要素が dict かつ 'language' キーを持ち、
          その値が allowed に含まれないものは除外
        - それ以外はそのまま保持
        - フィルタ後の要素を再帰的に処理して返す
    ・プリミティブはそのまま返す
    """
    if isinstance(obj, dict):
        return {k: filter_by_language(v, allowed) for k, v in obj.items()}
    if isinstance(obj, list):
        filtered = []
        for item in obj:
            if isinstance(item, dict) and "language" in item:
                if item["language"] not in allowed:
                    # 言語指定があって allowed にない→除外
                    continue
            # 辞書でもリストでもプリミティブでも保持
            filtered.append(item)
        # 絞り込んだあと、各要素を再帰処理
        return [filter_by_language(el, allowed) for el in filtered]
    return obj


idx = 1
idx_pad = str(idx).zfill(5)
file = SPECIES[idx_pad]
src_path = SPECIE_DIR_PATH / file

data = read_json(src_path)

result = strip_url(data)
result = collapse_name(result)
result = unwrap_single_dict_list(result)
result = filter_by_language(result)


dst_path = DEV_DIR_PATH / "sample.json"

write_json(result, dst_path)
