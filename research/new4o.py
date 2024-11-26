import asyncio
from multiprocessing import Process, Queue
from openai import AsyncOpenAI, AsyncStream
from speech_recognition import Recognizer, Microphone, RequestError, UnknownValueError
import numpy as np
from sounddevice import OutputStream
from piper.voice import PiperVoice


# Speak worker: runs in a separate process
def speak_worker(queue):
    model = "./pl_PL-darkman-medium.onnx"  # Piper model
    voice = PiperVoice.load(model)
    with OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16') as stream:
        while True:
            text = queue.get()
            if text == "STOP":
                break
            for audio_bytes in voice.synthesize_stream_raw(text):
                stream.write(np.frombuffer(audio_bytes, dtype=np.int16))
            print(f"Spoken: {text}")


# GPT text streaming and queueing sentences for speaking
async def handle_gpt_response(text_stream: AsyncStream, queue: Queue):
    sentence = ""
    async for chunk in text_stream:
        sentence += chunk.choices[0].delta.content or ""
        while "." in sentence:
            index = sentence.find(".")
            complete_sentence = sentence[:index + 1].strip()
            sentence = sentence[index + 1:]
            queue.put(complete_sentence)
    # Handle any leftover text
    if sentence.strip():
        queue.put(sentence.strip())


# Main asyncio loop
async def main():
    # Initialize components
    recognizer = Recognizer()
    client = AsyncOpenAI()
    queue = Queue()

    # Start speaking process
    speaking_process = Process(target=speak_worker, args=(queue,))
    speaking_process.start()

    try:
        with Microphone() as mic:
            while True:
                print("Waiting for button press...")
                if await button():  # Simulated button press
                    # Record and process audio
                    while True:
                        try:
                            audio = recognizer.listen(mic)
                            transcription = recognizer.recognize_google(audio, language="pl-PL")
                            print(f"Transcription: {transcription}")
                            break
                        except UnknownValueError:
                            print("Speech not recognized. Please try again.")
                        except RequestError as e:
                            print(f"Error with speech service: {e}")
                        except Exception as e:
                            print(f"Unexpected error: {e}")

                    # Send transcription to GPT
                    response_stream = await client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": transcription}],
                        stream=True,
                    )

                    # Stream GPT response and queue sentences for speech
                    await handle_gpt_response(response_stream, queue)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        queue.put("STOP")  # Signal speaking process to terminate
        speaking_process.join()


# Simulated button press (replace with real logic if needed)
async def button() -> bool:
    await asyncio.sleep(1)  # Simulate delay
    return True  # Simulate button press


# Run the program
if __name__ == "__main__":
    asyncio.run(main())
