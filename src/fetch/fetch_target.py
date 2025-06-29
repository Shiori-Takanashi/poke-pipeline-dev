# save_jsons.py
from __future__ import annotations
import asyncio
import aiohttp
import sqlite3
from typing import List, Tuple
from tqdm import tqdm
import aiofile
import json

from config.paths_anchor import JSON_DIR_PATH
from constants.target_names import FETCH_TARGET
from constants.base_url import BASE_URL


def get_name_and_url(base_url: str, fetch_target: List):
    names = []
    urls = []
    for target in fetch_target:
        names.append(target)
        url = base_url + target
        urls.append(url)
    return names, urls


async def fetch_all(urls: List[str], names: List[str]):
    semaphore = asyncio.Semaphore(50)
    async with aiohttp.ClientSession() as session:
        tasks_for_idxes = [
            fetch_endpoint_for_idxes(url, name, semaphore, session)
            for url, name in zip(urls, names)
        ]
        idxes_of_endpoints = await asyncio.gather(*tasks_for_idxes)

        tasks_for_data = []
        for url, name, idxes in zip(urls, names, idxes_of_endpoints):
            if idxes is None:
                continue
            for idx in idxes:
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
    retries: int = 5,
    timeout: int = 10,
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


async def fetch_endpoint_for_idxes(url: str, name: str, semaphore, session):
    full_url = f"{url}?limit=3000/"
    data = await fetch_json_with_retry(full_url, session, semaphore, name=name)
    if data is None:
        return None
    return [entry["url"].rstrip("/").split("/")[-1] for entry in data["results"]]


async def fetch_endpoint_for_data(
    url: str, name: str, idx: str, semaphore, session
) -> str | None:
    target_url = f"{url}{idx}/"
    data = await fetch_json_with_retry(target_url, session, semaphore, name=name)
    if data is None:
        return None

    output_dir = JSON_DIR_PATH / name
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = output_dir / f"{int(idx):05d}.json"
    async with aiofile.AIOFile(str(filename), "w") as af:
        await af.write(json.dumps(data, ensure_ascii=False, indent=2))
        await af.fsync()
    return str(filename)


if __name__ == "__main__":
    names, urls = get_name_and_url(BASE_URL, FETCH_TARGET)
    results = asyncio.run(fetch_all(urls, names))
    print(f"Saved {len(results)} JSON files")
    failed = sum(1 for r in results if r is None)
    print(f"Failed {failed} JSON files.")
