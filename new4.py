import asyncio
import os
from openai import AsyncOpenAI
from gtts import gTTS
import io
from pydub import AudioSegment
import simpleaudio as sa
import sounddevice as sd
import numpy as np

client = AsyncOpenAI()

async def get_text(prompt, text_queue):
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    buffer = ''
    async for chunk in response:
        content = chunk.choices[0].delta.content or ""
        if content:
            buffer += content
            # Check if buffer contains a sentence terminator
            while any(p in buffer for p in '.!?'):
                # Split at the first sentence terminator
                for i, c in enumerate(buffer):
                    if c in '.!?':
                        sentence = buffer[:i+1].strip()
                        buffer = buffer[i+1:].strip()
                        await text_queue.put(sentence)
                        break
    # Put any remaining text in the buffer
    if buffer:
        await text_queue.put(buffer)
    # Signal completion
    await text_queue.put(None)

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

# def play_sound(raw_data, channels, sample_width, frame_rate):
#     play_obj = sa.play_buffer(
#         raw_data,
#         num_channels=channels,
#         bytes_per_sample=sample_width,
#         sample_rate=frame_rate
#     )
#     play_obj.wait_done()

def play_sound(raw_data, channels, sample_width, frame_rate):
    # Convert raw_data to numpy array
    if sample_width == 2:  # 2 bytes per sample for 'int16'
        dtype = np.int16
    elif sample_width == 4:  # 4 bytes per sample for 'float32'
        dtype = np.float32
    else:
        raise ValueError(f"Unsupported sample width: {sample_width}")

    audio_array = np.frombuffer(raw_data, dtype=dtype)

    # Reshape array based on number of channels
    if channels > 1:
        audio_array = audio_array.reshape(-1, channels)
    else:
        audio_array = audio_array.reshape(-1)

    # Play audio using sounddevice
    sd.play(audio_array, samplerate=frame_rate)
    sd.wait()  # Wait until playback is finished

async def play_audio(audio_queue):
    loop = asyncio.get_running_loop()
    while True:
        audio_item = await audio_queue.get()
        if audio_item is None:
            break
        raw_data, channels, sample_width, frame_rate = audio_item
        # Play audio data in executor
        await loop.run_in_executor(None, play_sound, raw_data, channels, sample_width, frame_rate)

async def main():
    text_queue = asyncio.Queue()
    audio_queue = asyncio.Queue()
    prompt = "Provide me with an inspiring message about the beauty of nature."

    # Start coroutines
    await asyncio.gather(
        get_text(prompt, text_queue),
        text_to_speech(text_queue, audio_queue),
        play_audio(audio_queue),
    )

if __name__ == "__main__":
    asyncio.run(main())
