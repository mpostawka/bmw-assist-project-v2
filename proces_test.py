from multiprocessing import Process, Queue
import asyncio

def speak_worker(queue):
    import pyttsx3  # Example text-to-speech library
    tts_engine = pyttsx3.init()
    while True:
        text = queue.get()
        if text == "STOP":
            break
        tts_engine.say(text)
        tts_engine.runAndWait()

# Main asyncio program
async def main():
    from asyncio import Queue as AsyncQueue
    
    text_queue = Queue()
    speaking_process = Process(target=speak_worker, args=(text_queue,))
    speaking_process.start()

    async def generate_responses():
        sentences = ["Hello world.", "This is a test.", "Async programming is fun!"]
        for sentence in sentences:
            await asyncio.sleep(1)  # Simulate delay in ChatGPT response
            print(f"Generated sentence: {sentence}")
            text_queue.put(sentence)

    await generate_responses()
    text_queue.put("STOP")
    speaking_process.join()


asyncio.run(main())