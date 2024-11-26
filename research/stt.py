# import pyttsx3
import speech_recognition as sr

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Change speech rate
# engine.setProperty('rate', 180)

# # Get the avaiable voice
# voices = engine.getProperty('voices')

# # Choose a voice based on the voice id
# engine.setProperty('voice', voices[0].id) 

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio)
            print("Transcription:", transcription)
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))





#wait for users to say "Friday"
print("Say 'Friday' to start...")
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    while True:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            print("transcription:", transcription)
            pass
                        
        except Exception as e:
            print(f"An error occurred: {e}")