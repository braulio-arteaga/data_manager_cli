"""
exporter.py
Guarda los resultados en archivos JSON para poder revisarlos después.
"""

import json


def exportar_estadisticas(estadisticas, ruta_salida):
    # Usamos with para que el archivo se cierre aunque ocurra un error
    try:
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            json.dump(estadisticas, archivo, ensure_ascii=False, indent=2)
        print(f"  Estadísticas guardadas en: {ruta_salida}")
    except OSError as e:
        raise OSError(f"No se pudo guardar el archivo: {e}")


def exportar_registros(lista_registros, ruta_salida):
    try:
        with open(ruta_salida, "w", encoding="utf-8") as archivo:
            json.dump(lista_registros, archivo, ensure_ascii=False, indent=2)
        print(f"  Datos guardados en: {ruta_salida} ({len(lista_registros)} registros)")
    except OSError as e:
        raise OSError(f"No se pudo guardar el archivo: {e}")
