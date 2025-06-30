from __future__ import annotations

import sys
from pathlib import Path

import pytest

# --- モジュールパス追加（ルートディレクトリを sys.path に追加）---
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# --- テスト対象の関数をインポート ---
from util.re_endpoint_name import rename_endpoint_name


class TestRenameEndpointName:
    """rename_endpoint_name関数のテストクラス"""

    def test_rename_single_hyphen(self):
        """単一のハイフンをアンダースコアに変換するテスト"""
        result = rename_endpoint_name("pokemon-species")
        assert result == "pokemon_species"

    def test_rename_multiple_hyphens(self):
        """複数のハイフンをアンダースコアに変換するテスト"""
        result = rename_endpoint_name("pokemon-form-generation")
        assert result == "pokemon_form_generation"

    def test_rename_no_hyphen(self):
        """ハイフンがない場合のテスト"""
        result = rename_endpoint_name("pokemon")
        assert result == "pokemon"

    def test_rename_empty_string(self):
        """空文字列のテスト"""
        result = rename_endpoint_name("")
        assert result == ""

    def test_rename_only_hyphens(self):
        """ハイフンのみの文字列のテスト"""
        result = rename_endpoint_name("---")
        assert result == "___"

    def test_rename_hyphen_at_start(self):
        """文字列の最初にハイフンがある場合のテスト"""
        result = rename_endpoint_name("-pokemon")
        assert result == "_pokemon"

    def test_rename_hyphen_at_end(self):
        """文字列の最後にハイフンがある場合のテスト"""
        result = rename_endpoint_name("pokemon-")
        assert result == "pokemon_"

    def test_rename_consecutive_hyphens(self):
        """連続するハイフンのテスト"""
        result = rename_endpoint_name("pokemon--species")
        assert result == "pokemon__species"

    def test_rename_mixed_characters(self):
        """数字や他の文字が含まれる場合のテスト"""
        result = rename_endpoint_name("pokemon-form-123")
        assert result == "pokemon_form_123"

    def test_rename_with_uppercase(self):
        """大文字が含まれる場合のテスト"""
        result = rename_endpoint_name("Pokemon-Species")
        assert result == "Pokemon_Species"


# パラメータ化テストの例
@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("pokemon-species", "pokemon_species"),
        ("move-learn-method", "move_learn_method"),
        ("ability", "ability"),
        ("type", "type"),
        ("pokemon-form", "pokemon_form"),
        ("generation-v", "generation_v"),
        ("", ""),
        ("-", "_"),
        ("--", "__"),
        ("pokemon-", "pokemon_"),
        ("-pokemon", "_pokemon"),
    ],
)
def test_rename_endpoint_name_parametrized(input_str: str, expected: str):
    """パラメータ化テストによる複数パターンの検証"""
    result = rename_endpoint_name(input_str)
    assert result == expected
