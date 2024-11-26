text = "Cześć! Jak się masz?"

import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

model = "./pl_PL-darkman-medium.onnx"
voice = PiperVoice.load(model)

# Setup a sounddevice OutputStream with appropriate parameters
# The sample rate and channels should match the properties of the PCM data
stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
stream.start()
print("go")
for audio_bytes in voice.synthesize_stream_raw(text):
    int_data = np.frombuffer(audio_bytes, dtype=np.int16)
    stream.write(int_data)

stream.stop()
stream.close()