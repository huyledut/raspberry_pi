from gtts import gTTS
from playsound import playsound
import os

class TextToSpeech:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.fileName = "voice.mp3"
        self.tts = gTTS(text="None", lang="vi")

    def Read(self, message):
        self.tts.text = message
        self.tts.save(self.fileName)
        audio_file = os.path.join(os.path.dirname(__file__), "voice.mp3")
        playsound(audio_file)
        os.remove(audio_file)

ts = TextToSpeech()