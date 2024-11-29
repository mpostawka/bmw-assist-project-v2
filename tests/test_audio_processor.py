import asyncio
from unittest.mock import Mock

import pytest
from pydub import AudioSegment

from assist.assistant.audio.processor import AudioProcessor


@pytest.mark.asyncio
async def test_audio_processor() -> None:
    audio_queue: asyncio.Queue[AudioSegment | None] = asyncio.Queue()
    play_sound = Mock()

    await audio_queue.put(AudioSegment.silent(duration=1000))
    await audio_queue.put(None)

    audio_processor = AudioProcessor(play_sound)
    await audio_processor.play_audio(audio_queue)

    assert play_sound.call_count == 1
    assert audio_queue.qsize() == 0
