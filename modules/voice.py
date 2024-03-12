import pyttsx3

class WindowsTalker:
    # funcion que realiza que nuestro programa hable 
    def __init__(self):        
        self.engine = pyttsx3.init() # inicializa nuestra voz para el programa
        self.engine.setProperty('rate', 145) # modificaciones para ir mas lento o mas rapido
        self.voices = self.engine.getProperty('voices') # para cambiar la voz del programa
        self.engine.setProperty('voice', self.voices[3].id) # modificacion del tipo de voz
        
    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait() 

class Talker:
    def __init__(self, talker_cls):
        self.talker_cls = talker_cls
    def talk(self, text):
        self.talker_cls.talk(text)