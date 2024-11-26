from gtts import gTTS
import io
from pydub import AudioSegment

async def text_to_speech(text_queue, audio_queue):
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
        sound = AudioSegment.from_file(fp, format='mp3')
        raw_data = sound.raw_data
        # Prepare a tuple with raw data and audio parameters
        audio_item = (raw_data, sound.channels, sound.sample_width, sound.frame_rate)
        await audio_queue.put(audio_item)