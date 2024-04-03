import pandas as pd

df = pd.read_csv('datos.csv')

class BuscarPersona:
    def buscarExistencia(nombre):
        return len(df[df['nombre'] == nombre]['apellido_paterno'].values) > 0

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
