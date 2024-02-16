# Modelo deep learning
import asyncio # Llamadas asincronas
import websockets # sockets levanta el servidor
import numpy as np # Manejar arreglos
import torch # Tensores

from transformers import AutoModelForCTC, AutoProcessor # levantar el servidor con especificaciones de idioma
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor 

import argparse

# Variables globales
SERVER = 'localhost'
PORT = 8001
# modelos
ENGLISH_MODEL = 'facebook/wav2vec2-large-960h-lv60-self' # modelo en ingles
SPANISH_MODEL = 'jonatasgrosman/wav2vec2-large-xlsr-53-spanish' # modelo en español

# Controlador del servidor
class SpeechRecognitionServer:
    # Constructor, donde se valida si se inicializa con los parametros correctos
    def __init__(self, language: str):
        if language not in ('EN', 'ES'):
            raise ValueError(f'Language: {language}, not supported.')
        if language == 'EN':
            # variable model y proccessor 
            # Para ambos modelos estamos utilizando el modelo Wav2vec
            # es un modelo lanzado por facebook
            self.model = AutoModelForCTC.from_pretrained(ENGLISH_MODEL)
            self.processor = AutoProcessor.from_pretrained(ENGLISH_MODEL)
        elif language == 'ES':
            self.model = Wav2Vec2ForCTC.from_pretrained(SPANISH_MODEL)
            self.processor = Wav2Vec2Processor.from_pretrained(SPANISH_MODEL)

        run = websockets.serve(self.speechRecognition, SERVER, PORT)
        # Hacen que la función corra de manera continua
        asyncio.get_event_loop().run_until_complete(run)
        asyncio.get_event_loop().run_forever()

    
    # Levantar un servidor weebsocket, el cual recibira una cadena de bites, los transformara a un arreglo
    # con numpy, los transformará a un tensor y los pasara mediante un modelo de deep learning y retorna el texto
    async def speechRecognition(self, websocket):
        print(f'-> Client connection stablished.')
        try:
            while True:
                # recibe el mensaje
                message = await websocket.recv()
                # transformamos con numpy a un vector
                float64_buffer = np.frombuffer(message, dtype=np.int16) / 327767
                # Si este arreglo tiene contenido voz
                if len(float64_buffer) > 1:
                    # entonces se pasa a traves de una función de tensor
                    inputs = self.processor(torch.tensor(float64_buffer), sampling_rate=16_000, return_tensors='pt', paddung=True)
                    with torch.no_grad():
                        logits = self.model(inputs.input_values, attention_mask=inputs.attention_mask).logits

                    predicted_ids = torch.argmax(logits, dim=-1)
                    # contiene el texto
                    transcription = self.processor.batch_decode(predicted_ids)[0]
                    # envio de la respuesta
                    await websocket.send(transcription.lower()) 
                else:
                    await websocket.send("")

        except KeyboardInterrupt:
            await websocket.close()
            print(f'\nServer finalized')
        except websockets.exceptions.ConnectionClosedOK:
            print(f'<- Client connection finalized')
        except websockets.exceptions.ConnectionClosedError:
            print(f'\nWebsocket closed')
        except Exception:
            print(f'Server down')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", help = "Set language")
    args = parser.parse_args()

    s = SpeechRecognitionServer(language=args.language)