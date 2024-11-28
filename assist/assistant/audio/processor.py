import asyncio


class AudioProcessor:
    def __init__(self, play_sound: callable):
        self.play_sound = play_sound

    async def play_audio(self, audio_queue):
        loop = asyncio.get_running_loop()
        while True:
            audio_segment = await audio_queue.get()
            if audio_segment is None:
                break
            # Play audio data in executor
            await loop.run_in_executor(None, self.play_sound, audio_segment)
