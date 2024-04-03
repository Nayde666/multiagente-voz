import pyttsx3

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