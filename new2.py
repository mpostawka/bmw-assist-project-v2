import asyncio
from openai import AsyncOpenAI, AsyncStream
from speech_recognition import AudioData, Microphone, Recognizer, RequestError, UnknownValueError
from gtts import gTTS
import os

class VoiceStream:
    pass




async def button() -> str:
    return "pressed"

async def read_voice(recognizer, microphone: Microphone) -> AudioData:
    audio = recognizer.listen(microphone)
    return audio

async def parse_audio(recognizer, audio: AudioData) -> str:
    transcription = recognizer.recognize_google(audio, language='pl-PL')
    print("transcription:", transcription)
    return transcription

async def ask_gpt(client, text: str) -> AsyncStream:
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}],
        stream=True,
    )
    return stream

async def write(text_stream: AsyncStream) -> None:
    async for chunk in text_stream:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
    print("", flush=True)

async def speak_stream(text_stream: AsyncStream) -> None:
    async for chunk in text_stream:
        text = chunk.choices[0].delta.content or ""
        try:
            tts = gTTS(text=text, lang='pl', slow=False)
            tts.save("output.mp3")
            os.system("mpg321 output.mp3")
        except Exception as e:
            print(f"An error occurred: {e}")

async def speak(text_stream: AsyncStream) -> None:
    text = ""
    async for chunk in text_stream:
        text += chunk.choices[0].delta.content or ""
    try:
        tts = gTTS(text=text, lang='pl', slow=False)
        tts.save("output.mp3")
        os.system("mpg321 output.mp3")
    except Exception as e:
        print(f"An error occurred: {e}")



async def main():
    recognizer = Recognizer()
    client = AsyncOpenAI()
    with Microphone() as microphone:
        while True:
            button_status = await button()
            if button_status == "pressed":
                while True:
                    try:
                        audio = await read_voice(recognizer, microphone)
                        text = await parse_audio(recognizer, audio)
                        break
                    except UnknownValueError:
                        print("Speech recognition could not understand audio")
                    except RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    except Exception as e:
                        print(f"An error occurred: {e}")
                response_stream = await ask_gpt(client, text)
                await speak(response_stream)

asyncio.run(main())
    