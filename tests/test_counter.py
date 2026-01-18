import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from tokencalc.counter import TokenCounter


@pytest.fixture
def counter():
    # APIキーがなくても初期化できるようにモック
    with patch("anthropic.Anthropic"), patch("anthropic.AsyncAnthropic"), patch(
        "google.genai.Client"
    ), patch("tiktoken.encoding_for_model") as mock_tiktoken:
        # tiktokenの動作をモック
        mock_encoding = MagicMock()
        mock_encoding.encode.return_value = [1, 2, 3]  # 常に3トークン
        mock_tiktoken.return_value = mock_encoding

        c = TokenCounter()
        # 各種クライアントを手動でモックに置き換え
        c.anthropic_client = MagicMock()
        c.async_anthropic_client = AsyncMock()
        c.google_client = MagicMock()
        c.openai_encoding = mock_encoding
        return c


def test_count_openai_tokens(counter):
    assert counter.count_openai_tokens("hello") == 3


def test_count_anthropic_tokens_sync(counter):
    # 同期版Anthropicのモック
    mock_response = MagicMock()
    mock_response.input_tokens = 5
    counter.anthropic_client.beta.messages.count_tokens.return_value = mock_response

    assert counter.count_anthropic_tokens("hello") == 5


@pytest.mark.asyncio
async def test_count_anthropic_tokens_async(counter):
    # 非同期版Anthropicのモック
    mock_response = MagicMock()
    mock_response.input_tokens = 6
    counter.async_anthropic_client.beta.messages.count_tokens.return_value = (
        mock_response
    )

    count = await counter.async_count_anthropic_tokens("hello")
    assert count == 6


@pytest.mark.asyncio
async def test_get_all_counts_async(counter):
    # Anthropic非同期モック
    mock_anthropic = MagicMock()
    mock_anthropic.input_tokens = 10
    counter.async_anthropic_client.beta.messages.count_tokens.return_value = (
        mock_anthropic
    )

    # Google非同期モック (aio.models.count_tokens)
    mock_google = MagicMock()
    mock_google.total_tokens = 15
    counter.google_client.aio.models.count_tokens = AsyncMock(return_value=mock_google)

    counts = await counter.async_get_all_counts("test content")

    assert counts["anthropic"] == 10
    assert counts["openai"] == 3
    assert counts["google"] == 15
