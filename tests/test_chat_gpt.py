import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from assist.assistant.text_processor.chat_gpt import ChatGPT


@pytest.mark.asyncio
async def test_chat_gpt() -> None:
    text_queue: asyncio.Queue[str | None] = asyncio.Queue()
    prompt = "Tell me a joke."

    with patch("assist.assistant.text_processor.chat_gpt.AsyncOpenAI") as mock_AsyncOpenAI:
        mock_client = mock_AsyncOpenAI.return_value
        mock_response = AsyncMock()
        mock_response.__aiter__.return_value = [
            AsyncMock(choices=[AsyncMock(delta=AsyncMock(content="Why did the chicken cross the road?"))]),
            AsyncMock(choices=[AsyncMock(delta=AsyncMock(content="To get to the other side!"))]),
        ]
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        chat_gpt = ChatGPT()
        await chat_gpt.ask(prompt, text_queue)

        assert text_queue.qsize() == 3
        assert await text_queue.get() == "Why did the chicken cross the road?"
        assert await text_queue.get() == "To get to the other side!"
        assert await text_queue.get() is None
