from modules.brain import Escucha 
from modules.voice import Talker, WindowsTalker
from modules.nurse import FindDisease
from modules.finder import BuscarPersona
from modules.defaultMessages import AssistanMessages
import re as regex

talker = Talker(WindowsTalker())

def main():
    talker.talk(f"{AssistanMessages.mensajes_predeterminados('saludo')}")
    escucha = Escucha()
    try:
        response = escucha.listener()
        while not regex.match(".adios+|.adiós+", response):                    
            # nombre completo de la persona
            if "dime el nombre completo de" in response:
                talker.talk(f"Buscando...")
                person = response.replace("dime la información de", '').replace(".",'').strip()
                if BuscarPersona.buscarExistencia(person):
                    talker.talk(f"Su nombre completo es {person} {BuscarPersona.nombre_completo(person)}.")
                else:
                    talker.talk(f"No se encontro a la persona {person}.")
                    print(person)

            # fecha de nacimiento
            if "dime la fecha de nacimiento de" in response:
                talker.talk(f"Buscando...")
                person = response.replace("dime la fecha de nacimiento de", '').replace(".",'').strip()
                if BuscarPersona.buscarExistencia(person):
                    talker.talk(f"Su fecha de nacimiento es {BuscarPersona.buscar_edad(person)}.")
                else:
                    talker.talk(f"No se encontro a la persona {person}.")
                    print(person)
            
            #busqueda de genero
            if "dime el genero de" in response:
                talker.talk(f"Buscando...")
                person = response.replace("dime el genero de", '').replace(".",'').strip()
                if BuscarPersona.buscarExistencia(person):
                    talker.talk(f"Su genero es {BuscarPersona.buscar_genero(person)}.")
                else:
                    talker.talk(f"No se encontro a la persona {person}.")
                    print(person)
            
            #buscar su nua
            if "dime el nua de" in response:
                talker.talk(f"Buscando...")
                person = response.replace("dime el nua de", '').replace(".",'').strip()
                if BuscarPersona.buscarExistencia(person):
                    talker.talk(f"Su nau es {BuscarPersona.buscar_nua(person)}.")
                else:
                    talker.talk(f"No se encontro a la persona {person}.")
                    print(person)

            # modo enfermero
            if "me siento mal" in response:
                talker.talk(f"{AssistanMessages.mensajes_predeterminados('enfermedad')}")
                response = escucha.listener().replace('.','').strip()
                if FindDisease.findText(response):
                    recomendacion = FindDisease.findCure(response).toLower()
                    talker.talk(f"Puedes realizar lo siguiente, {recomendacion}")
                else:
                    talker.talk(f"{AssistanMessages.mensajes_predeterminados('sin informacion')}")
                
            else:
                talker.talk(f"No se a que se refiere por {response}")
                print(response)
            response = escucha.listener()
        talker.talk(f"{AssistanMessages.mensajes_predeterminados('despedida')}")
    except Exception as e:
        talker.talk(f"{AssistanMessages.mensajes_predeterminados('error')} {e}")
        print(e)


# entry point
if __name__ == '__main__':
    main()