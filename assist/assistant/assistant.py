import asyncio

from assistant.audio.processor import AudioProcessor


class Assistant():
    def __init__(self, tts, text_processor, audio_player: AudioProcessor):
        self.text_queue = asyncio.Queue()
        self.audio_queue = asyncio.Queue()
        self.tts = tts
        self.text_processor = text_processor #LLM
        self.audio_player = audio_player


    async def respond(self, command: str):
        await asyncio.gather(
            self.text_processor.ask(command, self.text_queue),
            self.tts(self.text_queue, self.audio_queue),
            self.audio_player.play_audio(self.audio_queue),
        )
