import asyncio
from assistant.assistant import Assistant
from assistant.audio.players.play_simpleaudio import play_simpleaudio
from assistant.audio.processor import AudioProcessor
from assistant.text_processor.chat_gpt import ChatGPT
from assistant.tts.google_tts import text_to_speech
from gather import gather_command


async def main():
    tts = text_to_speech
    text_processor = ChatGPT()
    audio_processor = AudioProcessor(play_simpleaudio)
    assistant = Assistant(tts, text_processor, audio_processor)

    for i in range(3): # while True:
        command = await gather_command()
        await assistant.respond(command)

if __name__ == "__main__":
    asyncio.run(main())