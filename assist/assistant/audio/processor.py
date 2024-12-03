import asyncio
from typing import Callable

from assistant.types import AudioQueue
from pydub import AudioSegment


class AudioProcessor:
    def __init__(self, play_sound: Callable[[AudioSegment], None]) -> None:
        self.play_sound = play_sound

    async def play_audio(self, audio_queue: AudioQueue) -> None:
        loop = asyncio.get_running_loop()
        while True:
            audio_segment = await audio_queue.get()
            if audio_segment is None:
                break
            # Play audio data in executor
            await loop.run_in_executor(None, self.play_sound, audio_segment)
