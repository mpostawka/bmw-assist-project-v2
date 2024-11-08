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
            return recognizer.recognize_google(audio)
        except:
            print("")
            #print('Skipping unknown error')


while True:

    #wait for users to say "Friday"
    print("Say 'Friday' to start...")
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            print("transcription:", transcription)
                        
        except Exception as e:
            print("An error occurred: {}".format(e))