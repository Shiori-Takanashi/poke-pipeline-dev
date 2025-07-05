# save_jsons.py
from __future__ import annotations
import asyncio
import aiohttp
from typing import List, Tuple
from tqdm import tqdm
import aiofile
import json
import sys

from config.constant import BASE_URL, SEMAPHORE_INT, RETRYS_INT, TIMEOUT_INT
from config.target import FETCH_TARGET
from config.dirpath import JSON_DIR_PATH

from util.re_endpoint_name import rename_endpoint_name
from util.directory import json_dir_maker_from_name
from scripts.logger_demo import setup_demo_logger

logger = setup_demo_logger(__name__)


def setup_sub_dir(names: List[str] = FETCH_TARGET) -> None:
    for name in names:
        dirname = f"raw_{name}"
        json_dir_maker_from_name(dirname)


def get_name_and_url(base_url: str = BASE_URL, fetch_target: List = FETCH_TARGET):
    """
    configからendpoint-nameとendpoint-urlを構築。
    引数はデフォルト指定してある。省略することを推奨。
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
):
    semaphore = asyncio.Semaphore(semaphore_int)
    async with aiohttp.ClientSession() as session:
        tasks_for_indices = [
            fetch_endpoint_for_indices(url, name, semaphore, session)
            for url, name in zip(urls, names)
        ]
        indices_of_endpoints = await asyncio.gather(*tasks_for_indices)

        tasks_for_data = []
        for url, name, indices in zip(urls, names, indices_of_endpoints):
            if indices is None:
                continue
            for idx in indices:
                tasks_for_data.append(
                    fetch_endpoint_for_data(url, name, idx, semaphore, session)
                )

        results = []
        for coro in tqdm(
            asyncio.as_completed(tasks_for_data), total=len(tasks_for_data)
        ):
            result = await coro
            results.append(result)
        return results


async def fetch_json_with_retry(
    url: str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    retries: int = RETRYS_INT,
    timeout: int = TIMEOUT_INT,
    name: str = "",
) -> dict | None:
    async with semaphore:
        for attempt in range(1, retries + 1):
            try:
                async with session.get(url, timeout=timeout) as res:
                    res.raise_for_status()
                    return await res.json()
            except Exception as e:
                print(f"[{name}] {attempt} failed: {e}")
        print(f"[{name}] Failed after {retries} retries: {url}")
        return None


async def fetch_endpoint_for_indices(url: str, name: str, semaphore, session):
    full_url = f"{url}?limit=3000/"
    data = await fetch_json_with_retry(full_url, session, semaphore, name=name)
    if data is None:
        return None
    return [entry["url"].rstrip("/").split("/")[-1] for entry in data["results"]]


async def fetch_endpoint_for_data(
    url: str, name: str, idx: str, semaphore, session
) -> str | None:
    target_url = f"{url}/{idx}/"
    data = await fetch_json_with_retry(target_url, session, semaphore, name=name)
    if data is None:
        return None

    output_dir = JSON_DIR_PATH / f"raw_{rename_endpoint_name(name)}"

    if not output_dir.exists():
        logger.debug(f"JSONディレクトリが存在しません。初期化が正しくありません。")
        sys.exit(1)

    filename = output_dir / f"{int(idx):05d}.json"
    async with aiofile.AIOFile(str(filename), "w") as af:
        await af.write(json.dumps(data, ensure_ascii=False, indent=2))
        await af.fsync()
    return str(filename)


if __name__ == "__main__":
    setup_sub_dir()
    names, urls = get_name_and_url(BASE_URL, FETCH_TARGET)
    results = asyncio.run(fetch_all(urls, names))
    print(f"Saved {len(results)} JSON files")
    failed = sum(1 for r in results if r is None)
    print(f"Failed {failed} JSON files.")
    print("\n".join(names))
