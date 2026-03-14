"""
File: validator.py
Objective: Validar que cada registro tenga datos correctos antes
           de procesarlos. Se separa de la lógica principal
           para que sea más fácil de testear.
"""

# Categorías oficiales según clasificación del SIDPOL (PNP)
MODALIDADES_VALIDAS = {"Extorsión", "Robo", "Hurto", "Estafa", "Homicidio", "Otros"}


def validar_registro(registro):
    # Sin distrito el registro no sirve para agrupar ni analizar
    if not registro["distrito"]:
        return False, "Distrito vacío"

    if registro["modalidad"] not in MODALIDADES_VALIDAS:
        return False, f"Modalidad inválida: {registro['modalidad']}"

    # Nos enfocamos en los últimos 5 años para facilitar el análisis
    if registro["anio"] < 2021 or registro["anio"] > 2026:
        return False, f"Año fuera de rango: {registro['anio']}"

    if registro["mes"] < 1 or registro["mes"] > 12:
        return False, f"Mes fuera de rango: {registro['mes']}"

    if registro["n_denuncias"] < 0:
        return False, f"Número de denuncias negativo: {registro['n_denuncias']}"

    return True, ""


def filtrar_validos(lista_registros):
    registros_validos = []
    errores_encontrados = []

    for i, registro in enumerate(lista_registros):
        es_valido, mensaje_error = validar_registro(registro)

        if es_valido:
            registros_validos.append(registro)
        else:
            errores_encontrados.append(f"Fila {i + 1}: {mensaje_error}")

    return registros_validos, errores_encontrados
