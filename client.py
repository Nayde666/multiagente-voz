# Importamos las librerias necesarias

# -------------------------------------------------
# Se usa para realizar reconocimiento de voz en python. 
# Escuchando la entrada de voz del usuario y convertirtiendola
# en texto.
# Trabaja el manejo de motores como: 
#   - Google Speech Recognition (el que usaremos)
#   - Microsoft Bing Recognition 
import speech_recognition as sr 
# Pandas es una libreria utilizada para el analisis y la manupulación
# de datos. Ayudandono a darle estructura a nuestro archivo csv y 
# hacer busquedas en el.
import pandas as pd
# Convertir el texto a voz
import pyttsx3

#libreria interfaz grafica
import tkinter as tk

# Cargamos el archivo csv (separado por comas) y lo que hacemos es
# convertirlo a un Data Frame ahora no solo serán datos separados
# convirtiendo cada columna en una serie con mayor relación, para 
# la busqueda.
df = pd.read_csv('datos.csv')


# -------------------------------------------------------------------------------------
# Función para buscar la fecha de nacimiento de una persona en el DataFrame
# recibe como parametro "nombre"
def buscar_fecha_nacimiento(nombre):
    # Esta parte del código selecciona todas las filas en el DataFrame df 
    # donde el valor en la columna 'nombre' coincide exactamente con el 
    # nombre proporcionado como argumento a la función.

    # Usamos values. Esta parte del código convierte los valores de la 
    # columna 'fecha_nacimiento' en un arreglo de numpy.
    resultado = df[df['nombre'] == nombre]['fecha_nacimiento'].values
    # Esta parte del código verifica si se encontraron resultados. 
    # Si la longitud del arreglo resultado es mayor que cero, 
    # significa que se encontraron fechas de nacimiento para la persona especificada.
    if len(resultado) > 0:
        # Si se encontraron resultados, esta parte del código 
        # devuelve la primera fecha de nacimiento encontrada
        return resultado[0] #[0] --> el primero
    else:
        # (si no) 
        # # retornamos un mensaje de aviso
        return "No se encontró la fecha de nacimiento para esa persona."


# -------------------------------------------------------------------------------------
# Función para buscar el apellido materno de una persona en el DataFrame
# recibe como parametro "nombre"
def buscar_apellido_materno(nombre):
    # Esta parte del código selecciona todas las filas en el DataFrame df 
    # donde el valor en la columna 'nombre' coincide exactamente con el 
    # nombre proporcionado como argumento a la función.

    # Usamos values. Esta parte del código convierte los valores de la 
    # columna 'apellido_materno' en un arreglo de numpy.
    resultado = df[df['nombre'] == nombre]['apellido_materno'].values
    # Esta parte del código verifica si se encontraron resultados. 
    # Si la longitud del arreglo resultado es mayor que cero, 
    # significa que se encontraron apellidos maternos para la persona especificada.
    if len(resultado) > 0:
        # Si se encontraron resultados, esta parte del código 
        # devuelve el primer apellido materno encontrado
        return resultado[0] #[0] --> el primero
    else:
        # (si no) 
        # # retornamos un mensaje de aviso
        return "No se encontró el apellido materno para esa persona."

def buscar_edad(nombre):
    
    resultado = df[df['nombre'] == nombre]['edad'].values

    if len(resultado) > 0:
        return resultado[0] 
    else:
        return "No se encontró la edad para esa persona."
    
def buscar_genero(nombre):
    
    resultado = df[df['nombre'] == nombre]['genero'].values

    if len(resultado) > 0:
        return resultado[0] 
    else:
        return "No se encontró el genero de esta persona."
    
def buscar_nua(nombre):
    resultado = df[df['nombre'] == nombre]['nua'].values
    if len(resultado) > 0:
        return resultado[0] 
    else:
        return "No se encontró el nua de esta persona."


#--------------------------------------------------------------------------------------
# Función para leer un texto con voz, recibira como parametro texto
def hablar(texto):
    # es una biblioteca de Python que proporciona una interfaz para el motor de texto a voz (TTS) eSpeak
    engine = pyttsx3.init() # inicializar el motor de síntesis de voz proporcionado por la biblioteca pyttsx3
    # Este método se utiliza para proporcionar el texto que se leerá en voz alta. 
    engine.say(texto)
    # Este método se llama después de engine.say(texto) para que el motor de texto a voz reproduzca el texto 
    # proporcionado y espere hasta que se complete la reproducción antes de continuar con lp demásdel codigo. 
    engine.runAndWait()

# crea un objeto de tipo Recognizer de la biblioteca speech_recognition
# Este objeto es esencialmente un reconocedor de voz que permite al programa
# interactuar con servicios de reconocimiento de voz
r = sr.Recognizer()


# ------------------------------------------------------------------------------------------------
# Función para escuchar y transcribir la voz
def escuchar():
    # Crea un contexto usando el micrófono como fuente de audio. 
    # Dentro de este contexto, todos los comandos relacionados con la
    # captura de audio se ejecutarán utilizando el micrófono como fuente.
    with sr.Microphone() as source:
        # Este comando ajusta el reconocedor (Recognizer) para el ruido de fondo presente en el entorno. 
        # Esto ayuda a mejorar la precisión del reconocimiento de voz al reducir el ruido externo y no
        # se vea afectada la capturación
        r.adjust_for_ambient_noise(source)  # Ajusta para el ruido de fondo
        hablar("Bienvenido a nuestro agente de voz")  # Lee con voz el mensaje de bienvenida
        print("Esperando instrucciones...") # mensaje 
        # Captura audio desde la fuente (en este caso, el micrófono) durante un período de tiempo 
        # Después de este tiempo (5s), si no se ha detectado ningún sonido, se generará una excepción.
        audio = r.listen(source, timeout=5)  # Ajustar el tiempo de grabación
    try:
        # Este comando utiliza la API de reconocimiento de voz de Google para transcribir el audio 
        # capturado (audio) en texto. La opción language="es-ES" se utiliza para especificar el 
        # idioma del audio capturado.
        texto = r.recognize_google(audio, language="es-ES")
        # CHECAR
        # Devuelve el texto transcribio convertido a minúsculas. 


        #return texto.lower()
        texto = texto.lower()
        # Verificamos si la instrucción contiene la frase específica para obtener la fecha de nacimiento
        if "dime la fecha de nacimiento de" in texto:
            hablar("Has dicho: " + texto)  # Lee con voz lo que se ha dicho, envia como argumento el texto
            return texto
        elif "dime el apellido materno de" in texto:  # Verifica si la instrucción contiene la frase para obtener el apellido materno
            hablar("Has dicho: " + texto)  # Lee con voz lo que se ha dichoenvia como argumento el texto
            return texto
        elif "dime la edad de" in texto:  # Verifica si la instrucción contiene la frase para obtener el apellido materno
            hablar("Has dicho: " + texto)  # Lee con voz lo que se ha dichoenvia como argumento el texto
            return texto
        elif "dime el género de" in texto:  # Verifica si la instrucción contiene la frase para obtener el apellido materno
            hablar("Has dicho: " + texto)  # Lee con voz lo que se ha dichoenvia como argumento el texto
            return texto
        elif "dime el número único de" in texto:  # Verifica si la instrucción contiene la frase para obtener el apellido materno
            hablar("Has dicho: " + texto)  # Lee con voz lo que se ha dichoenvia como argumento el texto
            return texto
       
        else:
            return None # Devolvemos None si la instrucción no coincide
    
    # Captura la excepción UnknownValueError, que se genera cuando el reconocedor 
    # de voz no puede entender lo que se dijo.
    except sr.UnknownValueError:
        hablar("No se pudo entender lo que dijiste")  # Lee con voz el mensaje de error
        print("No se pudo entender lo que dijiste")
        return "No se pudo entender lo que dijiste" # MENSAJE DE ALRTA

    # TENEMOS QUE TENER UNA CONEXION A INTERNET POR SER API
    # se genera cuando hay un error al recuperar los resultados 
    # del servicio de reconocimiento de voz (por ejemplo, problemas de conexión).
    except sr.RequestError as e:
        hablar("Error al recuperar resultados del servicio de reconocimiento de voz; {0}".format(e))  # Lee con voz el mensaje de error
        return "Error al recuperar resultados del servicio de reconocimiento de voz; {0}".format(e)

# Función principal de nuestro programa
def buscar():
    activado = True
    while True:
        if activado:
            comando = escuchar()
            if comando is not None:  # Verificamos si se reconoció una instrucción válida
                nombre = obtener_nombre(comando)
                if nombre != "desactivar":
                    if "apellido materno" in comando:
                        apellido_materno = buscar_apellido_materno(nombre)
                        hablar(f"El apellido materno de {nombre} es: {apellido_materno}")  # Lee con voz el resultado
                        print(f"El apellido materno de {nombre} es: {apellido_materno}")
                    elif "fecha de nacimiento" in comando:
                        fecha_nacimiento = buscar_fecha_nacimiento(nombre)
                        hablar(f"La fecha de nacimiento de {nombre} es: {fecha_nacimiento}")  # Lee con voz el resultado
                        print(f"La fecha de nacimiento de {nombre} es: {fecha_nacimiento}")
                    elif "edad" in comando:
                        edad = buscar_edad(nombre)
                        hablar(f"La edad de {nombre} es: {edad}")  # Lee con voz el resultado
                        print(f"La edad de {nombre} es: {edad}")
                    elif "género" in comando: 
                        género = buscar_genero(nombre)
                        hablar(f"El genero de {nombre} es: {género}")
                        print(f"El género de {nombre} es: {género}")
                    elif "número único" in comando: 
                        nua = buscar_nua(nombre)
                        hablar(f"El nua de {nombre} es: {nua}")
                        print(f"El nua de {nombre} es: {nua}")
                elif "desactivar" in comando:
                    activado = False
                    hablar("Agente desactivado.")  # Lee con voz el mensaje de desactivación
                    print("Agente desactivado.")
                    break
        else:
            comando = escuchar()
            if "activar" in comando:
                activado = True
                hablar("Agente activado. Esperando instrucciones...")  # Lee con voz el mensaje de activación
                print("Agente activado. Esperando instrucciones...")

# Función para obtener el nombre de la instrucción según corresponda
def obtener_nombre(comando):
    # Dividimos la cadena de texto comando en una lista de palabras utilizando el espacio como delimitador
    palabras = comando.split(" ")
    # Verificamos si la instrucción contiene la frase específica para obtener la fecha de nacimiento
    if "dime la fecha de nacimiento de" in comando:
        # Buscamos el índice de la segunda ocurrencia de la palabra "de" en la lista de palabras
        indice_de = [i for i, palabra in enumerate(palabras) if palabra == "de"][1]
    else:
        # Buscamos el índice de la primera ocurrencia de la palabra "de" en la lista de palabras
        indice_de = palabras.index("de")
    # El nombre se encuentra después de la palabra "de"
    nombre = " ".join(palabras[indice_de + 1:])
    return nombre.strip()  # Devolvemos el nombre extraído, eliminando cualquier espacio en blanco adicional
 
# define la funcion del boton y la accion de responder por voz la frase agente activado
def activar_agente():
    hablar("Agente activado. Esperando instrucciones...")
    print("Agente activado. Esperando instrucciones...")
    buscar()

# Interfaz gráfica
root = tk.Tk()  # ventana
root.title("Agente de voz") # nombre de la ventana
root.geometry("400x400") # dimensiones

# define el boton en la ventana y el comando que ejecutara
btn_activar = tk.Button(root, text="Activar agente", command=activar_agente)
btn_activar.pack(pady=20) # define las dimensiones del boton

root.mainloop() # hace un ciclo infinito para que la ventana no cierre a menos que se presione el boton "x"
