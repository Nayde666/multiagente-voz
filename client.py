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

# Cargamos el archivo csv (separado por comas) y lo que hacemos es
# convertirlo a un Data Frame ahora no solo serán datos separados
# convirtiendo cada columna en una serie con mayor relación, para 
# la busqueda.
df = pd.read_csv('datos.csv')

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

# crea un objeto de tipo Recognizer de la biblioteca speech_recognition
# Este objeto es esencialmente un reconocedor de voz que permite al programa
# interactuar con servicios de reconocimiento de voz
r = sr.Recognizer()

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
        return texto.lower()
    # Captura la excepción UnknownValueError, que se genera cuando el reconocedor 
    # de voz no puede entender lo que se dijo.
    except sr.UnknownValueError:
        return "No se pudo entender lo que dijiste" # MENSAJE DE ALRTA

    # TENEMOS QUE TENER UNA CONEXION A INTERNET POR SER API
    # se genera cuando hay un error al recuperar los resultados 
    # del servicio de reconocimiento de voz (por ejemplo, problemas de conexión).
    except sr.RequestError as e:
        return "Error al recuperar resultados del servicio de reconocimiento de voz; {0}".format(e)

# Función principal de nuestro programa
def main():
    activado = True  # Comienza en modo activado
    while True:
        if activado:
            comando = escuchar()
            print("Has dicho:", comando)
            nombre = obtener_nombre(comando)
            print("Nombre extraído:", nombre)  # Verificar el nombre extraído
            if nombre != "desactivar":
                fecha_nacimiento = buscar_fecha_nacimiento(nombre)
                print(f"La fecha de nacimiento de {nombre} es: {fecha_nacimiento}")
                # desactivar ejecución
            elif "desactivar" in comando:
                activado = False
                print("Agente desactivado.")
                break
        else:
            comando = escuchar()
            if "activar" in comando:
                activado = True
                print("Agente activado. Esperando instrucciones...")

# Funcion para busqueda
# recibe como parametro comando
def obtener_nombre(comando):
    # Divide la cadena de texto comando en una lista 
    # de palabras utilizando el espacio como delimitador. 
    # Esto separa la frase en palabras individuales.
    palabras = comando.split(" ")
    # Utiliza una comprensión de lista para encontrar todos los índices 
    # en la lista palabras donde el elemento sea igual a la palabra "de".
    # 
    # Esto encuentra todas las ocurrencias de la palabra "de" en la frase 
    # y devuelve sus índices en la lista
    indices_de = [i for i, palabra in enumerate(palabras) if palabra == "de"]
    # Verifica si hay al menos dos ocurrencias de la palabra "de" en la frase. 
    # Si hay menos de dos, significa que no hay suficientes ocurrencias 
    # para extraer un nombre.
    if len(indices_de) >= 2:
        # Si hay al menos dos ocurrencias de "de", esta línea toma todas las 
        # palabras que están después de la segunda ocurrencia de "de" y las 
        # une en un solo string. Método join() para 
        # unir las palabras y el slicing de lista para seleccionar las palabras correctas.
        nombre = " ".join(palabras[indices_de[1] + 1:])  
        # Devuelve el nombre extraído, eliminando cualquier espacio en blanco adicional 
        # al inicio y al final del nombre con el método strip()
        return nombre.strip()
    # Si no
    else:
        # Si hay menos de dos ocurrencias de "de", lo cual significa que no se puede extraer un nombre, 
        # devuelve una cadena vacía.
        return ""
        
if __name__ == "__main__":
    main()