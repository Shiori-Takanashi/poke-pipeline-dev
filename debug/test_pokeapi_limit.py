"""
PokeAPI の limit パラメータの挙動調査スクリプト

このスクリプトは、PokeAPIに対して異なるlimit値でリクエストを送信し、
レスポンスの挙動を調査します。特にlimit=3000の場合の動作を確認します。
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from pathlib import Path

# モジュールパス調整
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.constant import BASE_URL


async def test_single_limit(
    session: aiohttp.ClientSession, endpoint: str, limit: int = None
) -> dict:
    """単一のlimit値でAPIをテスト"""
    if limit is None:
        url = f"{BASE_URL}{endpoint}"
        test_name = "default"
    else:
        url = f"{BASE_URL}{endpoint}?limit={limit}"
        test_name = f"limit_{limit}"

    print(f"Testing {endpoint} with {test_name}: {url}")

    try:
        start_time = datetime.now()
        async with session.get(url, timeout=30) as response:
            end_time = datetime.now()
            data = await response.json()

            return {
                "test_name": test_name,
                "url": url,
                "status_code": response.status,
                "response_time_ms": (end_time - start_time).total_seconds() * 1000,
                "count": data.get("count"),
                "results_length": len(data.get("results", [])),
                "next": data.get("next"),
                "previous": data.get("previous"),
                "has_next": data.get("next") is not None,
                "first_result": (
                    data.get("results", [{}])[0] if data.get("results") else None
                ),
                "last_result": (
                    data.get("results", [{}])[-1] if data.get("results") else None
                ),
            }
    except asyncio.TimeoutError:
        return {"test_name": test_name, "url": url, "error": "Timeout (30s)"}
    except Exception as e:
        return {
            "test_name": test_name,
            "url": url,
            "error": str(e),
            "error_type": type(e).__name__,
        }


async def investigate_pokeapi_limits():
    """PokeAPIのlimitパラメータの挙動を詳細調査"""

    # テスト対象のエンドポイント
    endpoints = ["pokemon", "pokemon-species", "ability", "move"]

    # テストするlimit値
    limit_values = [
        None,  # デフォルト
        20,  # 小さい値
        100,  # 中程度
        1000,  # 大きい値
        3000,  # 現在使用中の値
        5000,  # より大きい値
        10000,  # 非常に大きい値
    ]

    all_results = {}

    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            print(f"\n=== Testing endpoint: {endpoint} ===")
            endpoint_results = []

            for limit in limit_values:
                result = await test_single_limit(session, endpoint, limit)
                endpoint_results.append(result)

                # 結果の簡易表示
                if "error" in result:
                    print(f"  {result['test_name']}: ERROR - {result['error']}")
                else:
                    print(
                        f"  {result['test_name']}: "
                        f"count={result['count']}, "
                        f"results={result['results_length']}, "
                        f"has_next={result['has_next']}, "
                        f"time={result['response_time_ms']:.1f}ms"
                    )

                # レート制限を避けるため少し待機
                await asyncio.sleep(10)

            all_results[endpoint] = endpoint_results

    return all_results


def analyze_results(results: dict) -> dict:
    """結果の分析を実行"""
    analysis = {}

    for endpoint, endpoint_results in results.items():
        analysis[endpoint] = {
            "summary": {},
            "limit_3000_details": None,
            "observations": [],
        }

        # limit=3000の詳細
        for result in endpoint_results:
            if result["test_name"] == "limit_3000" and "error" not in result:
                analysis[endpoint]["limit_3000_details"] = {
                    "total_count": result["count"],
                    "returned_count": result["results_length"],
                    "has_pagination": result["has_next"],
                    "response_time_ms": result["response_time_ms"],
                    "next_url": result["next"],
                }
                break

        # 各limit値での結果数比較
        for result in endpoint_results:
            if "error" not in result:
                limit_name = result["test_name"]
                analysis[endpoint]["summary"][limit_name] = {
                    "returned": result["results_length"],
                    "total": result["count"],
                    "has_next": result["has_next"],
                }

        # 観察事項
        limit_3000_result = analysis[endpoint]["limit_3000_details"]
        if limit_3000_result:
            if limit_3000_result["returned_count"] == limit_3000_result["total_count"]:
                analysis[endpoint]["observations"].append(
                    "limit=3000で全データを取得可能"
                )
            elif limit_3000_result["has_pagination"]:
                analysis[endpoint]["observations"].append(
                    "limit=3000でもページネーションが必要"
                )
            else:
                analysis[endpoint]["observations"].append("データ数がlimit値未満")

    return analysis


async def main():
    """メイン実行関数"""
    print("PokeAPI limit パラメータ挙動調査を開始...")
    print(f"Base URL: {BASE_URL}")

    # 調査実行
    results = await investigate_pokeapi_limits()

    # 分析実行
    analysis = analyze_results(results)

    # 結果をファイルに保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(__file__).parent.parent / "out"
    output_dir.mkdir(exist_ok=True)

    # 詳細結果
    results_file = output_dir / f"pokeapi_limit_investigation_{timestamp}.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # 分析結果
    analysis_file = output_dir / f"pokeapi_limit_analysis_{timestamp}.json"
    with open(analysis_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    # 簡易レポート
    report_file = output_dir / f"pokeapi_limit_report_{timestamp}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("PokeAPI Limit Parameter Investigation Report\n")
        f.write("=" * 50 + "\n\n")

        for endpoint, data in analysis.items():
            f.write(f"Endpoint: {endpoint}\n")
            f.write("-" * 30 + "\n")

            limit_3000 = data["limit_3000_details"]
            if limit_3000:
                f.write(f"Total items: {limit_3000['total_count']}\n")
                f.write(f"Returned with limit=3000: {limit_3000['returned_count']}\n")
                f.write(f"Pagination needed: {limit_3000['has_pagination']}\n")
                f.write(f"Response time: {limit_3000['response_time_ms']:.1f}ms\n")

            if data["observations"]:
                f.write("Observations:\n")
                for obs in data["observations"]:
                    f.write(f"  - {obs}\n")

            f.write("\n")

    print(f"\n=== 調査完了 ===")
    print(f"詳細結果: {results_file}")
    print(f"分析結果: {analysis_file}")
    print(f"レポート: {report_file}")

    # limit=3000の要約を表示
    print(f"\n=== limit=3000 要約 ===")
    for endpoint, data in analysis.items():
        limit_3000 = data["limit_3000_details"]
        if limit_3000:
            print(
                f"{endpoint}: {limit_3000['returned_count']}/{limit_3000['total_count']} "
                f"items (pagination: {limit_3000['has_pagination']})"
            )


if __name__ == "__main__":
    asyncio.run(main())
