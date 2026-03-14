"""
code: data_loader.py
objective: Carga el archivo CSV del SIDPOL y convierte cada fila en un
diccionario con los tipos de datos correctos (int, str).
"""

import csv


def cargar_datos(ruta_archivo):
    # Aquí guardamos todos los registros leídos
    lista_registros = []

    # Intentamos abrir el archivo. Si no existe, avisamos con un mensaje claro
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                # Convertimos los tipos porque el CSV los lee todo como texto
                registro = {
                    "anio": int(fila["anio"]),
                    "mes": int(fila["mes"]),
                    "departamento": fila["departamento"].strip(),
                    "provincia": fila["provincia"].strip(),
                    "distrito": fila["distrito"].strip(),
                    "ubigeo": fila["ubigeo"].strip(),
                    "modalidad": fila["modalidad"].strip(),
                    "n_denuncias": int(fila["n_denuncias"]),
                    "dist_emergencia": int(fila["dist_emergencia"]),
                }
                lista_registros.append(registro)

    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

    return lista_registros
