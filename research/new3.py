



for chunk in stream:
    text_queue.put(chunk)


def text_queue_consumer(text_queue):
    while True:
        chunk = text_queue.get()
        audio = text_to_speech(chunk)
        audio_queue.put(audio)

def audio_queue_consumer(audio_queue):
    with Stream() as stream:
        while True:
            audio = audio_queue.get()
            stream.put(audio)
