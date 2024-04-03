import speech_recognition as sr
import whisper
import os
import io # libreria para manipular el sistema operativo
import tempfile # para crear archivos y directorios temporales
from pydub import AudioSegment # Recoger informacion de audios grabados desde el microfono

temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav') 

listener = sr.Recognizer() 

class Escucha:
    # funcion para escuchar
    def __listen_from_mic(self):
        try:
            with sr.Microphone() as source:
                print("Di algo...")
                listener.adjust_for_ambient_noise(source) # ayudamos al programa a evitar el ruido de fondo y nos entienda mejor
                audio = listener.listen(source)
                data = io.BytesIO(audio.get_wav_data()) # con el audio vamos a crear un archivo tipo wap
                audio_clip = AudioSegment.from_file(data) # vamos a partir el audio en donde solamente nos escuchamos
                audio_clip.export(save_path, format='wav')
        except Exception as e:
            print(e)
        return save_path

    # funcion que reconoce el audio que creamos 
    def __recognize_audio(self, save_path):
        # el modelo puede depender de la potencia de la computadora que corra el programa, el default es base, pero se puede usar small, medium o large
        audio_model = whisper.load_model("small")
        transcription = audio_model.transcribe(save_path, language='spanish', fp16=False)
        return transcription["text"] 
    
    def listener(self):
        return self.__recognize_audio(self.__listen_from_mic()).lower()
