import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pydub import AudioSegment

from assist.assistant.tts.gTTS_wrapper import google_tts


@pytest.mark.asyncio
async def test_google_tts() -> None:
    text_queue: asyncio.Queue[str | None] = asyncio.Queue()
    audio_queue: asyncio.Queue[AudioSegment | None] = asyncio.Queue()

    await text_queue.put("Hello world.")
    await text_queue.put(None)

    with patch("assist.assistant.tts.gTTS_wrapper.gTTS") as mock_gTTS, patch(
        "assist.assistant.tts.gTTS_wrapper.AudioSegment"
    ) as mock_AudioSegment:

        mock_gTTS.return_value.write_to_fp = Mock()
        mock_AudioSegment.from_file.return_value = AudioSegment.silent(duration=1000)

        await google_tts(text_queue, audio_queue)

        assert not text_queue.qsize()
        assert audio_queue.qsize() == 2
        assert await audio_queue.get() is not None
        assert await audio_queue.get() is None
