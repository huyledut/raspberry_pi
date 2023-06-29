from gtts import gTTS
import os
import pygame
from time import sleep

class TextToSpeech:
    _instance = None
    __audio = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            pygame.init()
        return cls._instance

    def __init__(self):
        self.fileName = "voice.mp3"
        self.tts = gTTS(text="None", lang="vi")

    def Read(self, message):
        print("Lưu file âm thanh")
        if os.path.exists('voice.mp3'):
            os.remove('voice.mp3')
        self.tts.text = message
        self.tts.save(self.fileName)
        audio_file = os.path.join(os.path.dirname(__file__), "voice.mp3")
        print("Phát âm thanh")
        # Phát âm thanh
        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.play()
        print("Dang phat am thannh")
        # Kiểm tra xem âm thanh đang được phát hay không
        # while pygame.mixer.music.get_busy():
        #     sleep(0.1)
        os.remove(audio_file)
        sleep(0.5)

ts = TextToSpeech()