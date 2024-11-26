import pyttsx3
import time

# Initialize the TTS engine
engine = pyttsx3.init(driverName='espeak')

# Set the properties, such as voice and language (if supported)
voices = engine.getProperty('voices')
for voice in voices:
    if 'pl' in voice.languages or 'Polish' in voice.name:
        engine.setProperty('voice', voice.id)
        break

# Set the speaking rate if needed (optional)
engine.setProperty('rate', 150)

# Input text
engine.say("Cześć! Jak się masz?")
engine.runAndWait()
time.sleep(10)