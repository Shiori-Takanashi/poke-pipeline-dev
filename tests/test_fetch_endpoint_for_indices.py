import pytest
import asyncio
import aiohttp
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from src.fetch.fetch_target import fetch_endpoint_for_indices

response_data01 = {
    "count": 1000,
    "next" :
}


@pytest.fixture
def mock_session():
    """モックのセッションを作成"""
    session = AsyncMock()
    return session

@pytest.fixture
def mock_semaphore():
    """モックのセマフォを作成"""
    semaphore = AsyncMock()
    semaphore.__aenter__ = AsyncMock(return_value=None)
    semaphore.__aexit__ = AsyncMock(return_value=None)
    return semaphore

@pytest.mark.asyncio
async def test_successful_indices_extraction(mock_session, mock_semaphore):
    """正常なレスポンスからindicesを正しく抽出できることをテスト"""
    # モックレスポンスの準備
