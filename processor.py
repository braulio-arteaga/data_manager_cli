"""
processor.py
Funciones para filtrar, ordenar y calcular estadísticas de los registros.
Ninguna función usa input() para que puedan ser testeadas fácilmente.
"""


# ---------- FILTROS ----------

def filtrar_por_modalidad(lista_registros, modalidad):
    # Comparamos en minúsculas para que no importe si el usuario escribe
    # "robo", "Robo" o "ROBO"
    resultados = []
    for registro in lista_registros:
        if registro["modalidad"].lower() == modalidad.lower():
            resultados.append(registro)
    return resultados


def filtrar_por_anio(lista_registros, anio):
    resultados = []
    for registro in lista_registros:
        if registro["anio"] == anio:
            resultados.append(registro)
    return resultados


def filtrar_por_distrito(lista_registros, distrito):
    # los distritos en el CSV vienen en mayúsculas, así el usuario
    # puede escribir "miraflores" sin preocuparse
    resultados = []
    for registro in lista_registros:
        if registro["distrito"].lower() == distrito.lower():
            resultados.append(registro)
    return resultados


def filtrar_por_minimo_denuncias(lista_registros, minimo):
    resultados = []
    for registro in lista_registros:
        if registro["n_denuncias"] >= minimo:
            resultados.append(registro)
    return resultados


# ---------- ORDENAMIENTO ----------

def ordenar_por(lista_registros, campo, descendente=False):
    # Si la lista está vacía no hay nada que ordenar
    if not lista_registros:
        return []

    # Verificamos que el campo exista antes de ordenar
    if campo not in lista_registros[0]:
        raise KeyError(f"El campo '{campo}' no existe en los registros")

    return sorted(lista_registros, key=lambda registro: registro[campo], reverse=descendente)


# ---------- ESTADÍSTICAS ----------

def calcular_estadisticas(lista_registros):
    # Si no hay registros devolvemos todo en cero para no causar errores
    if not lista_registros:
        return {
            "total_registros": 0,
            "total_denuncias": 0,
            "promedio_denuncias": 0.0,
            "max_denuncias": 0,
            "min_denuncias": 0,
            "por_modalidad": {},
            "por_anio": {},
            "top5_distritos": {},
        }

    # Sacamos solo los números de denuncias para calcular max, min, suma
    denuncias = []
    for registro in lista_registros:
        denuncias.append(registro["n_denuncias"])

    total_denuncias = sum(denuncias)

    # Contamos cuántas denuncias hubo por cada modalidad
    por_modalidad = {}
    for registro in lista_registros:
        modalidad = registro["modalidad"]
        if modalidad not in por_modalidad:
            por_modalidad[modalidad] = 0
        por_modalidad[modalidad] += registro["n_denuncias"]

    # Contamos cuántas denuncias hubo por cada año
    por_anio = {}
    for registro in lista_registros:
        anio = registro["anio"]
        if anio not in por_anio:
            por_anio[anio] = 0
        por_anio[anio] += registro["n_denuncias"]

    # Contamos por distrito y nos quedamos con los 5 con más denuncias
    por_distrito = {}
    for registro in lista_registros:
        distrito = registro["distrito"]
        if distrito not in por_distrito:
            por_distrito[distrito] = 0
        por_distrito[distrito] += registro["n_denuncias"]

    distritos_ordenados = sorted(por_distrito.items(), key=lambda x: x[1], reverse=True)
    top5_distritos = dict(distritos_ordenados[:5])

    return {
        "total_registros": len(lista_registros),
        "total_denuncias": total_denuncias,
        "promedio_denuncias": round(total_denuncias / len(lista_registros), 2),
        "max_denuncias": max(denuncias),
        "min_denuncias": min(denuncias),
        "por_modalidad": por_modalidad,
        "por_anio": dict(sorted(por_anio.items())),
        "top5_distritos": top5_distritos,
    }
