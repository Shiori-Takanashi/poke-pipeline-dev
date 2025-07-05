from __future__ import annotations

# --- 標準ライブラリ ---
import sys
import json
import asyncio
import sqlite3
from pathlib import Path
from typing import List, Tuple

# --- サードパーティ ---
import aiohttp
import aiofile
import pytest
from tqdm import tqdm

# --- モジュールパス調整（ルート追加） ---
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# --- 自作モジュール ---
from config.constant import BASE_URL, SEMAPHORE_INT
from config.target import FETCH_TARGET
from config.dirpath import JSON_DIR_PATH
from src.fetch import fetch_target as ft
from src.fetch.fetch_target import (
    get_name_and_url,
    fetch_all,
    fetch_json_with_retry,
    fetch_endpoint_for_indices,
    fetch_endpoint_for_data,
)

# =====================================================================
#                           get_name_and_url
# =====================================================================


def test_get_name_and_url():
    """
    fetch_target.py の get_name_and_url() が、
    name, url のリストを正しく返すかを確認する。
    """
    names, urls = get_name_and_url()
    assert isinstance(names, list)
    assert isinstance(urls, list)
    assert len(names) == len(urls)


# =====================================================================
#                        fetch_json_with_retry
# =====================================================================


@pytest.mark.asyncio
async def test_fetch_json_with_retry_success():
    """
    正常なURLに対して、fetch_json_with_retry が JSON を返すことを確認。
    """
    url = "https://pokeapi.co/api/v2/ability/?limit=1"
    async with aiohttp.ClientSession() as session:
        sema = asyncio.Semaphore(SEMAPHORE_INT)
        data = await fetch_json_with_retry(url, session, sema, name="ability")
    assert data is not None
    assert "results" in data


@pytest.mark.asyncio
async def test_fetch_json_with_retry_failure():
    """
    存在しないURLに対して、fetch_json_with_retry が None を返すことを確認。
    """
    url = "https://pokeapi.co/api/v2/nonexistent/"
    async with aiohttp.ClientSession() as session:
        sema = asyncio.Semaphore(SEMAPHORE_INT)
        data = await fetch_json_with_retry(
            url, session, sema, retries=2, name="fail_test"
        )
    assert data is None


# =====================================================================
#                      fetch_endpoint_for_idxes
# =====================================================================


@pytest.mark.asyncio
async def test_fetch_endpoint_for_idxes_success():
    """
    正常なエンドポイントに対して、インデックスリストが取得できること。
    """
    url = "https://pokeapi.co/api/v2/ability"
    name = "ability"
    async with aiohttp.ClientSession() as session:
        sema = asyncio.Semaphore(SEMAPHORE_INT)
        idxes = await fetch_endpoint_for_idxes(url, name, sema, session)
    assert isinstance(idxes, list)
    assert all(isinstance(i, str) for i in idxes)


@pytest.mark.asyncio
async def test_fetch_endpoint_for_idxes_failure(monkeypatch):
    """
    異常系：fetch_json_with_retry をモックして None を返す async 関数を渡した場合
    fetch_endpoint_for_idxes は None を返すこと
    """

    async def fake_fetch_json(url, session, semaphore, name=""):
        return None

    monkeypatch.setattr(ft, "fetch_json_with_retry", fake_fetch_json)

    url = "https://pokeapi.co/api/v2/invalid"
    name = "invalid"
    async with aiohttp.ClientSession() as session:
        sema = asyncio.Semaphore(SEMAPHORE_INT)
        idxes = await fetch_endpoint_for_idxes(url, name, sema, session)
    assert idxes is None


# =====================================================================
#                            fetch_all
# =====================================================================


@pytest.mark.asyncio
async def test_fetch_all_combines_idx_and_data(monkeypatch):
    """
    fetch_all() が
      1) fetch_endpoint_for_idxes で得た idx 列
      2) fetch_endpoint_for_data で得た文字列
    を正しく組み合わせて返すこと。
    """

    async def fake_fetch_idx(url: str, name: str, sema, session):
        return ["01", "02"]

    async def fake_fetch_data(url: str, name: str, idx: str, sema, session):
        return f"{name}-{idx}"

    monkeypatch.setattr(ft, "fetch_endpoint_for_idxes", fake_fetch_idx)
    monkeypatch.setattr(ft, "fetch_endpoint_for_data", fake_fetch_data)

    names = ["alpha", "beta"]
    urls = ["http://example/alpha", "http://example/beta"]

    results = await fetch_all(urls, names, semaphore_int=1)
    expected = {f"{n}-{i}" for n in names for i in ["01", "02"]}
    assert set(results) == expected


# =====================================================================
#                    fetch_endpoint_for_data
# =====================================================================


@pytest.mark.asyncio
async def test_fetch_endpoint_for_data_success(tmp_path, monkeypatch):
    """
    fetch_json_with_retry が dict を返した場合、
    JSON_DIR_PATH/<name>/00001.json にファイルを書き、
    返り値はファイルパス文字列になること。
    """
    monkeypatch.setattr(ft, "JSON_DIR_PATH", tmp_path)
    monkeypatch.setattr(ft, "rename_endpoint_name", lambda name: name)

    sample = {"foo": "bar"}

    async def fake_fetch(url, session, semaphore, name=""):
        return sample

    monkeypatch.setattr(ft, "fetch_json_with_retry", fake_fetch)

    sema = asyncio.Semaphore(1)
    session = None
    idx = "1"

    result = await fetch_endpoint_for_data(
        "http://example/", "testname", idx, sema, session
    )

    path = Path(result)
    print(f"\n[DEBUG] output_dir.name: {path.parent.name}")  # 一時デバッグ用
    assert path.exists() and path.is_file()
    assert json.loads(path.read_text(encoding="utf-8")) == sample


@pytest.mark.asyncio
async def test_fetch_endpoint_for_data_failure(tmp_path, monkeypatch):
    """
    異常系：fetch_json_with_retry をモックして None を返す async 関数を渡した場合、
    ファイルを作らず None を返すこと
    """
    monkeypatch.setattr(ft, "JSON_DIR_PATH", tmp_path)

    async def fake_fetch_json(url, session, semaphore, name=""):
        return None

    monkeypatch.setattr(ft, "fetch_json_with_retry", fake_fetch_json)

    sema = asyncio.Semaphore(1)
    result = await fetch_endpoint_for_data("u/", "testname", "1", sema, None)

    assert result is None
    assert not (tmp_path / "testname").exists()
