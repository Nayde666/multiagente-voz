import pandas as pd
import json 
with open('assistan_message.json', 'r') as json_message:
    data_message = json.load(json_message)

normalized_messages_assistant = pd.json_normalize(data_message) 

class AssistanMessages:

    def mensajes_predeterminados(mensaje):
        return normalized_messages_assistant[normalized_messages_assistant['instruccion'] == mensaje]['mensaje'].values[0]
