import asyncio

from assistant import Assistant
from assistant.audio import AudioProcessor
from assistant.audio.players import play_simpleaudio
from assistant.text_processor import ChatGPT
from assistant.tts import google_tts
from gather import gather_command


async def main() -> None:
    tts = google_tts
    text_processor = ChatGPT()
    audio_processor = AudioProcessor(play_simpleaudio)
    assistant = Assistant(tts, text_processor, audio_processor)

    for i in range(3):  # while True:
        command = await gather_command()
        await assistant.respond(command)


if __name__ == "__main__":
    asyncio.run(main())
