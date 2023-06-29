from gtts import gTTS
import os
from pydub import AudioSegment
import simpleaudio as sa
from time import sleep

class TextToSpeech:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.fileName = "voice.wav"

    def Read(self, message):
        tts = gTTS(text=message, lang="vi")
        tts.save(self.fileName)
        audio_file = os.path.join(os.path.dirname(_file_), self.fileName)
        
        print("Phát âm thanh")
        # Load file âm thanh
        audio = AudioSegment.from_file(audio_file)
        
        # Chơi âm thanh
        play_obj = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
        play_obj.wait_done()
        
        # Xóa file âm thanh
        os.remove(audio_file)
        sleep(0.5)

ts = TextToSpeech