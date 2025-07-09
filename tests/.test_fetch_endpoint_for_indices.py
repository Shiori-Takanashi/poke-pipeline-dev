"""
fetch_endpoint_for_indices 関数専用のテスト

このモジュールは、src.fetch.fetch_target.fetch_endpoint_for_indices 関数の
単体テストを実行します。
"""

import pytest
import asyncio
import aiohttp
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
import sys

# モジュールパス調整
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.fetch.fetch_target import fetch_endpoint_for_indices


class TestFetchEndpointForIndices:
    """fetch_endpoint_for_indices 関数のテストクラス"""

    @pytest.fixture
    def mock_session(self):
        """モックのaiohttp.ClientSessionを作成"""
        session = AsyncMock()
        return session

    @pytest.fixture
    def mock_semaphore(self):
        """モックのasyncio.Semaphoreを作成"""
        semaphore = AsyncMock()
        semaphore.__aenter__ = AsyncMock(return_value=None)
        semaphore.__aexit__ = AsyncMock(return_value=None)
        return semaphore

    @pytest.mark.asyncio
    async def test_successful_indices_extraction(self, mock_session, mock_semaphore):
        """正常なレスポンスからindicesを正しく抽出できることをテスト"""
        # モックレスポンスの準備
        mock_response_data = {
            "results": [
                {"url": "https://pokeapi.co/api/v2/pokemon/1/"},
                {"url": "https://pokeapi.co/api/v2/pokemon/25/"},
                {"url": "https://pokeapi.co/api/v2/pokemon/150/"},
            ]
        }

        # fetch_json_with_retryをモック
        with patch(
            "src.fetch.fetch_target.fetch_json_with_retry",
            return_value=mock_response_data,
        ) as mock_fetch:

            result = await fetch_endpoint_for_indices(
                url="https://pokeapi.co/api/v2/pokemon",
                name="pokemon",
                semaphore=mock_semaphore,
                session=mock_session,
            )

            # 期待する結果
            expected = ["1", "25", "150"]
            assert result == expected

            # fetch_json_with_retryが正しいURLで呼ばれたかを確認
            mock_fetch.assert_called_once()
            call_args = mock_fetch.call_args[0]
            assert call_args[0] == "https://pokeapi.co/api/v2/pokemon?limit=3000/"

    @pytest.mark.asyncio
    async def test_url_parsing_edge_cases(self, mock_session, mock_semaphore):
        """URLパースのエッジケースをテスト"""
        # 末尾にスラッシュがない場合、複数スラッシュがある場合など
        mock_response_data = {
            "results": [
                {"url": "https://pokeapi.co/api/v2/pokemon/1"},  # スラッシュなし
                {"url": "https://pokeapi.co/api/v2/pokemon/25//"},  # 複数スラッシュ
                {"url": "https://pokeapi.co/api/v2/pokemon/100/"},  # 正常
            ]
        }

        with patch(
            "src.fetch.fetch_target.fetch_json_with_retry",
            return_value=mock_response_data,
        ):

            result = await fetch_endpoint_for_indices(
                url="https://pokeapi.co/api/v2/pokemon",
                name="pokemon",
                semaphore=mock_semaphore,
                session=mock_session,
            )

            expected = ["1", "25", "100"]
            assert result == expected

    @pytest.mark.asyncio
    async def test_empty_results(self, mock_session, mock_semaphore):
        """空のresultsリストの場合のテスト"""
        mock_response_data = {"results": []}

        with patch(
            "src.fetch.fetch_target.fetch_json_with_retry",
            return_value=mock_response_data,
        ):

            result = await fetch_endpoint_for_indices(
                url="https://pokeapi.co/api/v2/pokemon",
                name="pokemon",
                semaphore=mock_semaphore,
                session=mock_session,
            )

            assert result == []

    @pytest.mark.asyncio
    async def test_fetch_failure(self, mock_session, mock_semaphore):
        """fetch_json_with_retryがNoneを返す場合（失敗時）のテスト"""
        with patch("src.fetch.fetch_target.fetch_json_with_retry", return_value=None):

            result = await fetch_endpoint_for_indices(
                url="https://pokeapi.co/api/v2/pokemon",
                name="pokemon",
                semaphore=mock_semaphore,
                session=mock_session,
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_malformed_response(self, mock_session, mock_semaphore):
        """不正な形式のレスポンスの場合のテスト"""
        # resultsキーが存在しない
        mock_response_data = {"count": 1302, "next": None}

        with patch(
            "src.fetch.fetch_target.fetch_json_with_retry",
            return_value=mock_response_data,
        ):

            with pytest.raises(KeyError):
                await fetch_endpoint_for_indices(
                    url="https://pokeapi.co/api/v2/pokemon",
                    name="pokemon",
                    semaphore=mock_semaphore,
                    session=mock_session,
                )

    @pytest.mark.asyncio
    async def test_malformed_url_in_results(self, mock_session, mock_semaphore):
        """resultsの中にurlキーが存在しない場合のテスト"""
        mock_response_data = {
            "results": [
                {"name": "bulbasaur"},  # urlキーがない
                {"url": "https://pokeapi.co/api/v2/pokemon/2/"},
            ]
        }

        with patch(
            "src.fetch.fetch_target.fetch_json_with_retry",
            return_value=mock_response_data,
        ):

            with pytest.raises(KeyError):
                await fetch_endpoint_for_indices(
                    url="https://pokeapi.co/api/v2/pokemon",
                    name="pokemon",
                    semaphore=mock_semaphore,
                    session=mock_session,
                )

    @pytest.mark.asyncio
    async def test_different_endpoints(self, mock_session, mock_semaphore):
        """異なるエンドポイントでのテスト"""
        mock_response_data = {
            "results": [
                {"url": "https://pokeapi.co/api/v2/ability/1/"},
                {"url": "https://pokeapi.co/api/v2/ability/2/"},
                {"url": "https://pokeapi.co/api/v2/ability/3/"},
            ]
        }

        with patch(
            "src.fetch.fetch_target.fetch_json_with_retry",
            return_value=mock_response_data,
        ) as mock_fetch:

            result = await fetch_endpoint_for_indices(
                url="https://pokeapi.co/api/v2/ability",
                name="ability",
                semaphore=mock_semaphore,
                session=mock_session,
            )

            expected = ["1", "2", "3"]
            assert result == expected

            # 正しいURLが構築されているかを確認
            call_args = mock_fetch.call_args[0]
            assert call_args[0] == "https://pokeapi.co/api/v2/ability?limit=3000/"

    @pytest.mark.asyncio
    async def test_large_indices(self, mock_session, mock_semaphore):
        """大きなindices値の処理テスト"""
        mock_response_data = {
            "results": [
                {"url": "https://pokeapi.co/api/v2/pokemon/10001/"},
                {"url": "https://pokeapi.co/api/v2/pokemon/99999/"},
            ]
        }

        with patch(
            "src.fetch.fetch_target.fetch_json_with_retry",
            return_value=mock_response_data,
        ):

            result = await fetch_endpoint_for_indices(
                url="https://pokeapi.co/api/v2/pokemon",
                name="pokemon",
                semaphore=mock_semaphore,
                session=mock_session,
            )

            expected = ["10001", "99999"]
            assert result == expected

    @pytest.mark.asyncio
    async def test_url_construction(self, mock_session, mock_semaphore):
        """URLの構築が正しく行われることをテスト"""
        mock_response_data = {"results": []}

        with patch("src.fetch.fetch_target.fetch_json_with_retry") as mock_fetch:
            await fetch_endpoint_for_indices(
                url="https://example.com/api/test",
                name="test",
                semaphore=mock_semaphore,
                session=mock_session,
            )

            # limit=3000/が正しく付加されているかを確認
            call_args = mock_fetch.call_args[0]
            assert call_args[0] == "https://example.com/api/test?limit=3000/"


# 単体実行用
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
