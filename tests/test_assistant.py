from unittest.mock import AsyncMock

import pytest

from assist.assistant.assistant import Assistant


@pytest.mark.asyncio
async def test_assistant() -> None:
    tts = AsyncMock()
    text_processor = AsyncMock()
    audio_player = AsyncMock()

    assistant = Assistant(tts, text_processor, audio_player)

    command = "Tell me a joke."
    await assistant.respond(command)

    assert text_processor.ask.call_count == 1
    assert tts.call_count == 1
    assert audio_player.play_audio.call_count == 1
