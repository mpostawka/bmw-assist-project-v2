import io

from gtts import gTTS
from pydub import AudioSegment


async def google_tts(text_queue, audio_queue):
    while True:
        sentence = await text_queue.get()
        if sentence is None:
            # Signal completion
            await audio_queue.put(None)
            break
        # Generate audio data
        tts = gTTS(sentence)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        # Use pydub to read mp3 data
        audio_segment = AudioSegment.from_file(fp, format="mp3")
        await audio_queue.put(audio_segment)
