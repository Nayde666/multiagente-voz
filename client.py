#1 Identificar entrada de audio con PyAudio
#2 Set parametros de streaming
#3 web socket client

import pyaudio # Es para reconocer la interfaz de la entrada de audio
import asyncio
import webrtcvad # detecta si es voz 
import websockets

import sounddevice as sd

CHANNELS = 1 # cantidad de canales, mono 
RATE = 16000 # numero de muestras por segundo, 16000 por los modelos del servidor
FRAME_DURATION = 20 # Determinar la duración
FORMAT = pyaudio.paInt16
CHUNK = int(RATE * FRAME_DURATION / 1000) # documentación de pyaudio
# --------------------------------
INPUT_DEVICE = 'Nay (AMD Audio Device)'

SERVER = "ws://localhost:8001"

vad = webrtcvad.Vad()
vad.set_mode(1)

class SpeechRecognitionClient:
    def __init__(self):
        self.transcript = ""
        self.audio = pyaudio.PyAudio()

        self.getAudioInterface()
        self.setStreamSettings()

        asyncio.run(self.startStream())

        self.stream.close()
        self.audio.terminate()

    # 3
    async def startStream(self):
        async with websockets.connect(SERVER) as websocket:
            frames = b''
            try:
                while True:
                    frame = self.stream.read(CHUNK, exception_on_overflow=False)
                    if vad.is_speech(frame, RATE):
                        frames += frame
                    elif len(frames) > 1:
                        await websocket.send(frames)
                        frames = b''

                        text = await websocket.recv()
                        self.transcript = f"{self.transcript} {text}" if len(text) > 1 else self.transcript
                        print(f'> {self.transcript}')



            except KeyboardInterrupt:
                await websocket.close()
                print(f'\nWebsocket closed.')
            except websockets.exceptions.ConnectionClosedError:
                print(f'\nWebsocket closed.')
            except Exception:
                print(f'\nWebsocket closed.')
            finally:
                print('*'*50)
                print(f'\nTranscript: \n\n{self.transcript}\n')
    # 2 
    def setStreamSettings(self):
        self.stream = self.audio.open(
            input_device_index = self.inputDevice,
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = CHUNK
        )
    # 1
    def getAudioInterface(self):
        # Definimos el dispositivo de entrada (se detectan)
        self.inputDevice = None
        numDevices = self.audio.get_host_api_info_by_index(0)["deviceCount"]
        for index in range(numDevices):
            name = self.audio.get_device_info_by_host_api_device_index(0, index).get("name")
            if name == INPUT_DEVICE:
                self.inputDevice = index
                break

        if self.inputDevice is None:
            raise ValueError(f'Audio device "{INPUT_DEVICE}" was not found.')

if __name__ == '__main__':
    def list_audio_devices():
        audio = pyaudio.PyAudio()
        num_devices = audio.get_device_count()
        
        print("Lista de dispositivos de audio:")
        for i in range(num_devices):
            device_info = audio.get_device_info_by_index(i)
            device_name = device_info["name"]
            print(f"{i}: {device_name}")
        
        audio.terminate()

    list_audio_devices()
    # list_audio_devices
    s = SpeechRecognitionClient()