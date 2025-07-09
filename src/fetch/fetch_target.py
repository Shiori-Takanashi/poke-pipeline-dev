# fetch_target.py
"""
PokeAPIからデータを並行取得してJSONファイルとして保存するモジュール

このモジュールは以下の機能を提供します：
- 設定されたエンドポイントからデータの並行取得
- 取得したデータのJSONファイルとしての保存
- リトライ機能付きの堅牢な HTTP リクエスト処理
"""
from __future__ import annotations

import asyncio
import json
import sys
from typing import List

import aiofile
import aiohttp
from tqdm import tqdm

from config.constant import BASE_URL, SEMAPHORE_INT, RETRYS_INT, TIMEOUT_INT
from config.dirpath import JSON_DIR_PATH
from config.target import FETCH_TARGET, MONSTER_TARGET
from scripts.logger_demo import setup_demo_logger
from util.directory import json_dir_maker_from_name
from util.re_endpoint_name import rename_endpoint_name


logger = setup_demo_logger(__name__)


def setup_sub_dir(names: List[str] = FETCH_TARGET) -> None:
    """
    取得対象のエンドポイント用のサブディレクトリを作成する

    Args:
        names: 取得対象のエンドポイント名のリスト
    """
    for name in names:
        dirname = f"raw_{name}"
        json_dir_maker_from_name(dirname)


def get_name_and_url(
    base_url: str = BASE_URL, fetch_target: List[str] = FETCH_TARGET
) -> tuple[List[str], List[str]]:
    """
    configからendpoint-nameとendpoint-urlを構築

    Args:
        base_url: ベースとなるAPI URL
        fetch_target: 取得対象のエンドポイント名のリスト

    Returns:
        エンドポイント名のリストとURLのリストのタプル
    """
    names = []
    urls = []
    for target in fetch_target:
        names.append(target)
        url = base_url + target
        urls.append(url)
    return names, urls


async def fetch_all(
    urls: List[str], names: List[str], semaphore_int: int = SEMAPHORE_INT
) -> List[str | None]:
    """
    すべてのエンドポイントからデータを並行取得する

    Args:
        urls: 取得するURLのリスト
        names: エンドポイント名のリスト
        semaphore_int: 並行実行数の制限

    Returns:
        保存されたファイルパスのリスト（失敗時はNone）
    """
    semaphore = asyncio.Semaphore(semaphore_int)
    async with aiohttp.ClientSession() as session:
        # 最初にインデックス情報を取得
        tasks_for_indices = [
            fetch_endpoint_for_indices(url, name, session, semaphore)
            for url, name in zip(urls, names)
        ]
        indices_of_endpoints = await asyncio.gather(*tasks_for_indices)

        # インデックス情報を基に個別データを取得
        tasks_for_data = []
        for url, name, indices in zip(urls, names, indices_of_endpoints):
            if indices is None:
                continue
            for idx in indices:
                tasks_for_data.append(
                    fetch_endpoint_for_data(url, name, idx, session, semaphore)
                )

        # プログレスバー付きで並行実行
        results = []
        for coro in tqdm(
            asyncio.as_completed(tasks_for_data),
            total=len(tasks_for_data),
            desc="Fetching data"
        ):
            result = await coro
            results.append(result)
        return results



async def fetch_json_with_retry(
    url: str,
    name: str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    retries: int = RETRYS_INT,
    timeout: int = TIMEOUT_INT,
) -> dict | None:
    """
    リトライ機能付きでJSONデータを取得する

    Args:
        url: 取得するURL
        name: ログ用のエンドポイント名
        session: aiohttp クライアントセッション
        semaphore: 並行実行制御用セマフォ
        retries: リトライ回数
        timeout: タイムアウト秒数

    Returns:
        取得したJSONデータまたはNone（失敗時）
    """
    async with semaphore:
        for attempt in range(1, retries + 1):
            try:
                async with session.get(url, timeout=timeout) as res:
                    res.raise_for_status()
                    return await res.json()
            except Exception as e:
                logger.warning(f"[{name}] Attempt {attempt} failed: {e}")
        logger.error(f"[{name}] Failed after {retries} retries: {url}")
        return None


async def fetch_endpoint_for_indices(
    url: str, name: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore
) -> List[str] | None:
    """
    エンドポイントからインデックス一覧を取得する

    Args:
        url: エンドポイントのURL
        name: エンドポイント名
        session: aiohttp クライアントセッション
        semaphore: 並行実行制御用セマフォ

    Returns:
        インデックスのリストまたはNone（失敗時）
    """
    initial_url = f"{url}?limit=50/"
    next_url = None
    all_indices = []
    while True:
        if next_url:
            target_url = next_url
        else:
            target_url = initial_url

        data = await fetch_json_with_retry(target_url, name, session, semaphore)

        if data is None:
            logger.error(f"エンドポイント{name}のインデックス取得に失敗: {url}")
            return None

        indicies = [entry["url"].rstrip("/").split("/")[-1] for entry in data["results"]]
        all_indices.extend(indicies)

        next_url = data.get("next", None)

        if not next_url and not len(all_indices):
            logger.error(f"エンドポイント{name}のインデックスが取得できませんでした: {url}")
            return None

        if not next_url and len(all_indices) == data["count"]:
            logger.info(f"エンドポイント{name}のインデックス取得完了: {len(all_indices)}件")
            break

    return all_indices


async def fetch_endpoint_for_data(
    url: str,
    name: str,
    idx: str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
) -> str | None:
    """
    指定されたインデックスのデータを取得してファイルに保存する

    Args:
        url: エンドポイントのベースURL
        name: エンドポイント名
        idx: データのインデックス
        session: aiohttp クライアントセッション
        semaphore: 並行実行制御用セマフォ

    Returns:
        保存されたファイルパスまたはNone（失敗時）
    """
    target_url = f"{url}/{idx}/"
    data = await fetch_json_with_retry(target_url, name, session, semaphore)
    if data is None:
        return None

    output_dir = JSON_DIR_PATH / f"raw_{rename_endpoint_name(name)}"

    if not output_dir.exists():
        logger.error(f"JSONディレクトリが存在しません: {output_dir}")
        logger.error("setup_sub_dir() が正しく実行されていない可能性があります")
        sys.exit(1)

    filename = output_dir / f"{int(idx):05d}.json"
    try:
        async with aiofile.AIOFile(str(filename), "w") as af:
            await af.write(json.dumps(data, ensure_ascii=False, indent=2))
            await af.fsync()
        logger.debug(f"Saved: {filename}")
        return str(filename)
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        return None


if __name__ == "__main__":
    logger.info("データ取得処理を開始します")

    # サブディレクトリの初期化
    setup_sub_dir()
    logger.info("サブディレクトリを初期化しました")

    # エンドポイント名とURLの取得
    names, urls = get_name_and_url(BASE_URL, MONSTER_TARGET)
    logger.info(f"取得対象エンドポイント: {', '.join(names)}")

    # データの並行取得
    results = asyncio.run(fetch_all(urls, names))

    # 結果の集計と出力
    successful = sum(1 for r in results if r is not None)
    failed = sum(1 for r in results if r is None)

    logger.info(f"取得完了: 成功 {successful} 件, 失敗 {failed} 件")
    print(f"Saved {successful} JSON files")
    if failed > 0:
        print(f"Failed {failed} JSON files.")
    print(f"Target endpoints: {', '.join(names)}")
