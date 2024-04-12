import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

class GoogleTalker:
    def talk(self,text):
        self.tts = gTTS(text=text , lang="es")
        self.tts.save("audio.mp3")
        self.audio = AudioSegment.from_file("audio.mp3", format="mp3")
        play(self.audio)

class WindowsTalker:
    def __init__(self):        
        self.engine = pyttsx3.init() # inicializa nuestra voz para el programa
        self.engine.setProperty('rate', 145) # modificaciones para ir mas lento o mas rapido
        self.voices = self.engine.getProperty('voices') # para cambiar la voz del programa
    def talk(self, text):
        self.engine.say(text)  # Aquí podría ser donde se está agregando la exclamación
        self.engine.runAndWait() 

class Talker:
    def __init__(self, talker_cls):
        self.talker_cls = talker_cls
    def talk(self, text):
        self.talker_cls.talk(text)