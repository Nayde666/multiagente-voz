import tkinter as tk
from tkinter import scrolledtext
import sys
import io
import re as regex
import json
import string
from modules.brain import FasterEscucha
from modules.voice import Talker, WindowsTalker, GoogleTalker
from modules.defaultMessages import AssistanMessages
import matplotlib.pyplot as plt  # Importar matplotlib

def limpiar_respuesta(response, eliminar_acentos=False):
    # limpia la respuesta del usuario eliminando signos de puntuación y exclamación, y espacios al inicio y al final. 
    response = response.translate(str.maketrans('', '', string.punctuation)).replace('¡', '').replace('!', '').strip()
    if eliminar_acentos: 
        response = response.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    # ya no se manda lower porque desde el modulo brain se manda un resultado en lower
    return response

def main():
    # crear la ventana principal de Tkinter
    app = tk.Tk()
    app.title("Output Window")
    app.geometry("800x600")

    # crear el widget de texto para mostrar las impresiones
    output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=100, height=40)
    output_text.pack(fill=tk.BOTH, expand=True)

    # clase para capturar las impresiones
    class PrintCapture(io.StringIO):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.text_widget = output_text  # Asignar el widget de texto
            self.text_widget.configure(state='normal')  # Habilitar la edición del widget

        def write(self, s):
            super().write(s)
            if self.text_widget:
                self.text_widget.insert(tk.END, s)
                self.text_widget.see(tk.END)
                plt.pause(0.01)  # Pausar para actualizar la interfaz gráfica

    # Redirigir stdout a PrintCapture
    sys.stdout = PrintCapture()

    # cargar archivos
    with open('enfermedades.json', 'r') as diseases_file:
        diseases_data = json.load(diseases_file)

    with open('medicamentos.json', 'r') as medications_file:
        medications_data = json.load(medications_file)

    # Iniciar la interacción con el asistente
    talker = Talker(WindowsTalker())
    talker.talk(f"{AssistanMessages.mensajes_predeterminados('saludo')}")
    escucha = FasterEscucha()
    try:
        response = escucha.newListener()
        print(response)
        while not regex.match(".adios+|.adiós+", response):
            if "me siento mal" in response or "conozco la enfermedad que tengo" in response or "dime la función de este medicamento" in response:
                if "me siento mal" in response:
                    talker.talk("¿Cuántos síntomas tienes?")
                    responseDiseases = limpiar_respuesta(escucha.newListener())
                    print(responseDiseases)
                    try:
                        num_ciclos = int(responseDiseases)
                    except ValueError:
                        talker.talk("No entendí cuántos síntomas tienes. Intenta nuevamente.")
                        responseDiseases = limpiar_respuesta(escucha.newListener())
                        continue

                    sintomas_usuario = []
 
                    for i in range(num_ciclos):
                        talker.talk(f"Dime el síntoma {i+1}:")
                        responseDiseases = limpiar_respuesta(escucha.newListener())
                        print(responseDiseases)
                        sintomas_usuario.append(responseDiseases)

                    enfermedad_encontrada = None
                    for disease in diseases_data:
                        if all(sintoma in disease['sintomas'] for sintoma in sintomas_usuario):
                            enfermedad_encontrada = disease
                            break

                    if enfermedad_encontrada:
                        talker.talk(f"Has mencionado los siguientes síntomas: {', '.join(sintomas_usuario)}")
                        print(f"Has mencionado los siguientes síntomas: {', '.join(sintomas_usuario)}")
                        talker.talk(f"Podrías tener {enfermedad_encontrada['enfermedad']}.")
                        print(f"Podrías tener {enfermedad_encontrada['enfermedad']}.")
                        talker.talk(f"La solución recomendada es: {enfermedad_encontrada['soluciones']}")
                        print(f"La solución recomendada es: {enfermedad_encontrada['soluciones']}")

                        for medication in medications_data:
                            if medication['enfermedad'] == enfermedad_encontrada['enfermedad']:
                                talker.talk(f"El medicamento recomendado es {medication['medicamento']}.")
                                print(f"El medicamento recomendado es {medication['medicamento']}.")
                                talker.talk(f"Descripción: {medication['descripcion']}")
                                print(f"Descripción: {medication['descripcion']}")
                    else:
                        talker.talk(f"Los sintomas mencionados son {sintomas_usuario}")
                        talker.talk("No puedo identificar la enfermedad. Te recomiendo que consultes a un médico.")

                elif "conozco la enfermedad que tengo" in response:
                    talker.talk("¿Qué enfermedad tienes?")
                    enfermedad_usuario = limpiar_respuesta(escucha.newListener())
                    print(enfermedad_usuario)
                    medicamento_encontrado = next((medication for medication in medications_data if medication['enfermedad'] == enfermedad_usuario), None)
                    if medicamento_encontrado:
                        talker.talk(f"Para tu enfermedad '{enfermedad_usuario}' te recomendamos tomar {medicamento_encontrado['descripcion']}")
                        print(f"Para tu enfermedad '{enfermedad_usuario}' te recomendamos tomar {medicamento_encontrado['descripcion']}")
                        break
                    else:
                        talker.talk(f"Lo siento, no se encontró un medicamento asociado a esa enfermedad. '{enfermedad_usuario}'")

                elif "dime la función de este medicamento" in response:
                    talker.talk("¿Cuál es tu medicamento?")
                    medicamento_usuario = limpiar_respuesta(escucha.newListener())
                    
                    info_medicamento = next((medication for medication in medications_data if medication['medicamento'].lower() == medicamento_usuario), None)
                    if info_medicamento:
                        talker.talk(f"El medicamento {info_medicamento['medicamento']} sirve para {info_medicamento['enfermedad']}. {info_medicamento['descripcion']}")
                        print(f"El medicamento {info_medicamento['medicamento']} sirve para {info_medicamento['enfermedad']}. {info_medicamento['descripcion']}")
                        break
                    else:
                        talker.talk("Lo siento, no se encontró información sobre ese medicamento.")
                        talker.talk(f'El medicamento que mencionaste es: {medicamento_usuario}')
                        print(f'El medicamento que mencionaste es: {medicamento_usuario}')
                        break
            else:
                talker.talk(f"No entiendo lo que quieres decir con '{response}'")
                break
        talker.talk(f"{AssistanMessages.mensajes_predeterminados('despedida')}")
    except Exception as e:
        talker.talk(f"{AssistanMessages.mensajes_predeterminados('error')} {e}")
        print(e)

    # app.mainloop()

# entry point
if __name__ == '__main__':
    main()
