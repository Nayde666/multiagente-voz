from modules.brain import Escucha 
from modules.voice import Talker, WindowsTalker
import pandas as pd
import re as regex

import json 
with open('assistan_message.json', 'r') as json_message:
    data_message = json.load(json_message)

df = pd.read_csv('datos.csv')
normalized_messages_assistant = pd.json_normalize(data_message)

talker = Talker(WindowsTalker())

def nombre_completo(nombre):
    if len(df[df['nombre'] == nombre]['apellido_paterno'].values) > 0:
        return df[df['nombre'] == nombre]['apellido_paterno'].values[0] + ' ' + df[df['nombre'] == nombre]['apellido_materno'].values[0]
    else:
        return "No se encontro a la persona."

def buscar_fecha_de_nacimiento(nombre):
    if len(df[df['nombre'] == nombre]['fecha_nacimiento'].values) > 0: 
        return df[df['nombre'] == nombre]['fecha_nacimiento'].values[0]
    else:
        return "No se encontro a la persona."

def buscar_edad(nombre):
    if len(df[df['nombre'] == nombre]['edad'].values) > 0: 
        return df[df['nombre'] == nombre]['edad'].values[0]
    else:
        return "No se encontro a la persona."

def buscar_genero(nombre):
    if len(df[df['nombre'] == nombre]['genero'].values) > 0: 
        return df[df['nombre'] == nombre]['genero'].values[0]
    else:
        return "No se encontro a la persona."

def buscar_nua(nombre):
    if len(df[df['nombre'] == nombre]['nua'].values) > 0: 
        return df[df['nombre'] == nombre]['nua'].values[0]
    else:
        return "No se encontro a la persona."

def mensajes_predeterminados(mensaje):
    return normalized_messages_assistant[normalized_messages_assistant['instruccion'] == mensaje]['mensaje'].values[0]

def main():
    talker.talk(f"{mensajes_predeterminados('saludo')}")
    escucha = Escucha()
    try:
        response = escucha.listener()
        while not regex.match(".adios+|.adiós+", response):                    
            if "dime el nombre completo de" in response:
                talker.talk(f"Buscando...")
                person = response.replace("dime la información de", '').replace(".",'').strip()
                if len(df[df['nombre'] == person]['genero'].values) > 0:
                    talker.talk(f"Su nombre completo es {person} {nombre_completo(person)}.")
                else:
                    talker.talk(f"No se encontro a la persona {person}.")
                    print(person)
            if "dime el nombre completo de" in response:
                talker.talk(f"Buscando...")
                person = response.replace("dime la información de", '').replace(".",'').strip()
                if len(df[df['nombre'] == person]['genero'].values) > 0:
                    talker.talk(f"Su nombre completo es {person} {nombre_completo(person)}.")
                else:
                    talker.talk(f"No se encontro a la persona {person}.")
                    print(person)
            else:
                talker.talk(f"No se a que se refiere por {response}")
                print(response)
            response = escucha.listener()
        talker.talk(f"{mensajes_predeterminados('despedida')}")
    except Exception as e:
        talker.talk(f"{mensajes_predeterminados('error')} {e}")
        print(e)

# entry point
if __name__ == '__main__':
    main()