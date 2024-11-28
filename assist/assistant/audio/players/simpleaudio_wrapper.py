import simpleaudio as sa
from pydub import AudioSegment


def play_simpleaudio(audio: AudioSegment) -> None:
    play_obj = sa.play_buffer(
        audio_data=audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate,
    )
    play_obj.wait_done()
