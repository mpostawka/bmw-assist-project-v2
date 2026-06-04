import asyncio

from assistant import Assistant
from assistant.audio import AudioProcessor
from assistant.audio.players import play_simpleaudio
from assistant.screen import Screen, Visualizer
from assistant.text_processor import ChatGPT
from assistant.tts import google_tts
from gather import Gatherer


async def main() -> None:
    tts = google_tts
    text_processor = ChatGPT()

    with Screen() as screen, Gatherer(device_index=1) as gatherer:
        audio_processor = AudioProcessor(play_simpleaudio, Visualizer(screen))
        assistant = Assistant(tts, text_processor, audio_processor)
        for i in range(3):  # while True:
            command = gatherer.listen()  # Od razu szłyszy odpowiedź (od samego początku)
            await assistant.respond(command)


if __name__ == "__main__":
    asyncio.run(main())
