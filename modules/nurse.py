import pandas as pd

class FindDisease:
    def findText(disease):
        normalized_messages_assistant = pd.read_json("enfermedades.json")
        return len(normalized_messages_assistant[normalized_messages_assistant['enfermedad'] == disease]) > 0

    def findCure(disease):
        normalized_messages_assistant = pd.read_json("enfermedades.json")
        return normalized_messages_assistant[normalized_messages_assistant['enfermedad'] == disease].values[0]
    