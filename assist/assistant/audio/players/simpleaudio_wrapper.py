import simpleaudio as sa
from pydub import AudioSegment

def play_simpleaudio(audio: AudioSegment):
    play_obj = sa.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate
    )
    play_obj.wait_done()