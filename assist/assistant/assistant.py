import asyncio
from typing import Any, Callable, Coroutine

from assistant.audio.processor import AudioProcessor
from assistant.text_processor import TextProcessor
from pydub import AudioSegment

TextQueue = asyncio.Queue[str | None]
AudioQueue = asyncio.Queue[AudioSegment | None]


class Assistant:
    def __init__(
        self,
        tts: Callable[[TextQueue, AudioQueue], Coroutine[Any, Any, None]],
        text_processor: TextProcessor,
        audio_player: AudioProcessor,
    ) -> None:
        self.text_queue: TextQueue = asyncio.Queue()
        self.audio_queue: AudioQueue = asyncio.Queue()
        self.tts = tts
        self.text_processor = text_processor  # LLM
        self.audio_player = audio_player

    async def respond(self, command: str) -> None:
        await asyncio.gather(
            self.text_processor.ask(command, self.text_queue),
            self.tts(self.text_queue, self.audio_queue),
            self.audio_player.play_audio(self.audio_queue),
        )
