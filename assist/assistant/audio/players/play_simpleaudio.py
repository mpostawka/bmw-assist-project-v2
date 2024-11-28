import simpleaudio as sa

def play_simpleaudio(raw_data, channels, sample_width, frame_rate):
    play_obj = sa.play_buffer(
        raw_data,
        num_channels=channels,
        bytes_per_sample=sample_width,
        sample_rate=frame_rate
    )
    play_obj.wait_done()