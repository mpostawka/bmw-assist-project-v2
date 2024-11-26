import asyncio
import openai
from multiprocessing import Process, Queue

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'  # Replace with your actual API key

# Speech Recognition Process
def speech_recognition_worker(queue):
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    print("Speech recognition process started")
    with microphone as source:
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source)
                print("Recognizing...")
                text = recognizer.recognize_google(audio, language='pl-PL')
                print(f"Recognized: {text}")
                queue.put(text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

# Text-to-Speech Process
def text_to_speech_worker(queue):
    import logging
    import sys
    import io
    from gtts import gTTS
    from pydub import AudioSegment
    from pydub.playback import play

    # Set up logging to ensure messages are printed from the subprocess
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
    logger = logging.getLogger()

    logger.info("Text-to-speech process started")
    while True:
        text = queue.get()
        if text == "STOP":
            break
        try:
            tts = gTTS(text=text, lang='pl')
            with io.BytesIO() as f:
                tts.write_to_fp(f)
                f.seek(0)
                audio = AudioSegment.from_file(f, format="mp3")
                play(audio)
            logger.info(f"Spoken: {text}")
        except Exception as e:
            logger.error(f"An error occurred in TTS: {e}")

# Function to process ChatGPT response and send sentences to TTS
async def process_chatgpt_response(text_to_speech_queue, response_stream):
    sentence = ""
    async for chunk in response_stream:
        content = chunk.choices[0].delta.content or ""
        sentence += content
        print(content, end='', flush=True)
        while '.' in sentence:
            index = sentence.find('.')
            to_speak = sentence[:index+1].strip()
            sentence = sentence[index+1:]
            text_to_speech_queue.put(to_speak)
    # Send any remaining text
    if sentence.strip():
        text_to_speech_queue.put(sentence.strip())

# Main Function
async def main():
    text_input_queue = Queue()
    text_output_queue = Queue()

    # Start Speech Recognition and Text-to-Speech Processes
    speech_recognition_process = Process(target=speech_recognition_worker, args=(text_input_queue,))
    text_to_speech_process = Process(target=text_to_speech_worker, args=(text_output_queue,))

    speech_recognition_process.start()
    text_to_speech_process.start()

    client = openai.AsyncOpenAI()

    try:
        while True:
            # Asynchronously get text from the speech recognition process
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(None, text_input_queue.get)
            print(f"\nReceived from speech recognition: {text}\n")

            # Send text to ChatGPT and process the streaming response
            response_stream = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": text}],
                stream=True,
            )
            await process_chatgpt_response(text_output_queue, response_stream)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        text_output_queue.put("STOP")
        speech_recognition_process.terminate()
        text_to_speech_process.join()
        speech_recognition_process.join()

if __name__ == "__main__":
    asyncio.run(main())
