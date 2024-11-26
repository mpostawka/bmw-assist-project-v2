import asyncio
from openai import AsyncOpenAI, AsyncStream
from speech_recognition import AudioData, Microphone, Recognizer, RequestError, UnknownValueError
from gtts import gTTS
import numpy as np
from sounddevice import OutputStream
from piper.voice import PiperVoice
import os

from multiprocessing import Process, Queue

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

# async def speak_stream(text_stream: AsyncStream) -> None:
#     async for chunk in text_stream:
#         text = chunk.choices[0].delta.content or ""
#         try:
#             tts = gTTS(text=text, lang='pl', slow=False)
#             tts.save("output.mp3")
#             os.system("mpg321 output.mp3")
#         except Exception as e:
#             print(f"An error occurred: {e}")

# async def speak_gtts(text_stream: AsyncStream) -> None:
#     text = ""
#     async for chunk in text_stream:
#         text += chunk.choices[0].delta.content or ""
#     try:
#         tts = gTTS(text=text, lang='pl', slow=False)
#         tts.save("output.mp3")
#         os.system("mpg321 output.mp3")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# async def speak_gtts_improved(text_stream: AsyncStream) -> None:
#     sentence = ""
#     async for chunk in text_stream:
#         sentence += chunk.choices[0].delta.content or ""
#         if "." in sentence:
#             index = sentence.find(".")
#             to_speak = sentence[:index]
#             sentence = sentence[index+1:]
#             try:
#                 tts = gTTS(text=to_speak, lang='pl', slow=False)
#                 tts.save("output.mp3")
#                 os.system("mpg321 output.mp3")
#             except Exception as e:
#                 print(f"An error occurred: {e}")

# async def speak_piper(voice: PiperVoice, output_stream: OutputStream, text_stream: AsyncStream) -> None:
#     sentence = ""
#     async for chunk in text_stream:
#         sentence += chunk.choices[0].delta.content or ""
#         if "." in sentence:
#             index = sentence.find(".")
#             to_speak = sentence[:index]
#             sentence = sentence[index+1:]
#             for audio_bytes in voice.synthesize_stream_raw(to_speak):
#                 int_data = np.frombuffer(audio_bytes, dtype=np.int16)
#                 output_stream.write(int_data)

async def speak(queue: Queue, text_stream: AsyncStream) -> None:
    sentence = ""
    async for chunk in text_stream:
        sentence += chunk.choices[0].delta.content or ""
        if "." in sentence:
            index = sentence.find(".")
            to_speak = sentence[:index]
            sentence = sentence[index+1:]
            queue.put(to_speak)


############ SEPARATE PROCESS ############

def speak_worker(queue):
    import numpy as np
    from sounddevice import OutputStream
    from piper.voice import PiperVoice
    model = "./pl_PL-darkman-medium.onnx"
    voice = PiperVoice.load(model)
    with OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16') as stream:
        while True:
            text = queue.get()
            if text == "STOP":
                break
            for audio_bytes in voice.synthesize_stream_raw(text):
                int_data = np.frombuffer(audio_bytes, dtype=np.int16)
                stream.write(int_data)
            print(text)

############ SEPARATE PROCESS ############


async def main():
    recognizer = Recognizer()
    client = AsyncOpenAI()
    # model = "./pl_PL-darkman-medium.onnx"
    # voice = PiperVoice.load(model)
    # with OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16') as stream:
    text_queue = Queue()
    speaking_process = Process(target=speak_worker, args=(text_queue,))
    speaking_process.start()
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
                await speak(text_queue, response_stream)
                # await speak(voice, stream, response_stream)
    text_queue.put("STOP")
    speaking_process.join()

asyncio.run(main())
    