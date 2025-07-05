from typing import Any, Dict, List
from util.io_json import read_json, write_json
from pathlib import Path


class JsonTransformer:
    """JSONデータの変換処理を行うクラス"""

    def __init__(self):
        # 共通の無視キーを定義
        self.strip_ignore_keys = ["flavor_text_entries", "varieties"]
        self.filter_ignore_keys = ["flavor_varieties"]

    def strip_url(self, obj, under_varieties=False):
        """varietiesの下以外でURLキーを削除する"""
        if isinstance(obj, dict):
            cleaned = {}
            for key, value in obj.items():
                if key in self.strip_ignore_keys and key != "varieties":
                    continue
                is_under_varieties = under_varieties or (key == "varieties")
                if key == "url" and not is_under_varieties:
                    continue
                cleaned[key] = self.strip_url(value, is_under_varieties)
            return cleaned

        elif isinstance(obj, list):
            return [self.strip_urls(item, under_varieties) for item in obj]

        else:
            return obj

    def collapse_name(self, obj):
        """name のみを持つ辞書を文字列に変換する"""
        if isinstance(obj, dict):
            # 最小辞書かどうか判定
            if set(obj.keys()) == {"name"}:
                return obj["name"]
            return {k: self.collapse_name(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.collapse_name(item) for item in obj]
        return obj

    def unwrap_single_dict_list(self, obj):
        """
        リスト内に単一のネストされていない辞書しかない場合、
        [ { ... } ] → { ... } にアンラップする。
        それ以外は再帰的に走査してそのまま返す。
        """
        if isinstance(obj, dict):
            return {k: self.unwrap_single_dict_list(v) for k, v in obj.items()}

        if isinstance(obj, list):
            if (
                len(obj) == 1
                and isinstance(obj[0], dict)
                and all(not isinstance(v, (dict, list)) for v in obj[0].values())
            ):
                return self.unwrap_single_dict_list(obj[0])
            return [self.unwrap_single_dict_list(item) for item in obj]
        return obj

    def filter_by_language(self, obj, allowed=("ja", "ja-Hrkt")):
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
            filtered_dict = {}
            for k, v in obj.items():
                # ignore_keysに含まれるキーはスキップ
                if k in self.filter_ignore_keys:
                    continue
                filtered_dict[k] = self.filter_by_language(v, allowed)
            return filtered_dict

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
            return [self.filter_by_language(el, allowed) for el in filtered]
        return obj

    def latest_ja_flavor_text(entries: List[Dict]) -> Dict[str, str]:
        result, latest = {}, -1
        for e in entries:
            if not is_ja(e):
                continue
            v_id = extract_version_id(e.get("version", {}).get("url", ""))
            if v_id > latest:
                latest = v_id
                result["flavor_text"] = e.get("flavor_text", "")
        return result

    def all_transform(self, data):
        """すべての変換処理を順次実行する"""
        result = self.strip_url_except_in_varieties(data)
        result = self.collapse_name(result)
        result = self.unwrap_single_dict_list(result)
        result = self.filter_by_language(result)
        return result
