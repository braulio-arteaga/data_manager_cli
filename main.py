"""
================================================================
  UNIVERSIDAD NACIONAL DE INGENIERÍA
  Facultad de Economía, Estadística y Ciencias Sociales
  Pre-Maestría MSc. Ingeniería Estadística
================================================================
  Curso    : Introducción a la Programación en Python y PyTorch
  Profesor : Jorge Guevara
  Alumno   : Marden Braulio Arteaga Lescano
  Fecha    : 13 de marzo de 2026
----------------------------------------------------------------
  Proyecto : DataManager CLI
  Fuente   : Sistema Informático de Denuncias Policiales (SIDPOL)
  Objetivo : Procesamiento y análisis descriptivo de denuncias
             en Lima Metropolitana del periodo 2021 a 2026
  Uso      : python main.py
================================================================
"""

import sys
import os

from data_loader import cargar_datos
from validator import filtrar_validos
from processor import (
    filtrar_por_modalidad,
    filtrar_por_anio,
    filtrar_por_distrito,
    filtrar_por_minimo_denuncias,
    ordenar_por,
    calcular_estadisticas,
)
from exporter import exportar_estadisticas, exportar_registros
from utils import imprimir_tabla, imprimir_estadisticas, pedir_opcion, pedir_entero


# Rutas de archivos
RUTA_CSV          = os.path.join(os.path.dirname(__file__), "data", "denuncias_lima.csv")
RUTA_ESTADISTICAS = os.path.join(os.path.dirname(__file__), "data", "estadisticas.json")
RUTA_RESULTADOS   = os.path.join(os.path.dirname(__file__), "data", "resultados.json")

MODALIDADES  = ["Extorsión", "Robo", "Hurto", "Estafa", "Homicidio", "Otros"]
CAMPOS_ORDEN = ["anio", "mes", "distrito", "modalidad", "n_denuncias"]


def menu_filtrar(vista_actual):
    print("\n  Filtrar por:")
    print("  1 - Modalidad")
    print("  2 - Año")
    print("  3 - Distrito")
    print("  4 - Mínimo de denuncias")
    print("  0 - Volver")

    opcion = pedir_opcion("  Elige: ", ["0", "1", "2", "3", "4"])

    if opcion == "0":
        return vista_actual

    if opcion == "1":
        for i, modalidad in enumerate(MODALIDADES, 1):
            print(f"  {i} - {modalidad}")
        numero = pedir_entero("  Número de modalidad: ", 1, len(MODALIDADES))
        modalidad_elegida = MODALIDADES[numero - 1]
        resultado = filtrar_por_modalidad(vista_actual, modalidad_elegida)

    elif opcion == "2":
        anio = pedir_entero("  Año (2021-2026): ", 2021, 2026)
        resultado = filtrar_por_anio(vista_actual, anio)

    elif opcion == "3":
        distrito = input("  Nombre del distrito: ").strip()
        resultado = filtrar_por_distrito(vista_actual, distrito)

    elif opcion == "4":
        minimo = pedir_entero("  Mínimo de denuncias: ", 0)
        resultado = filtrar_por_minimo_denuncias(vista_actual, minimo)

    print(f"\n  Se encontraron {len(resultado)} registros.")
    return resultado


def menu_ordenar(vista_actual):
    print("\n  Ordenar por:")
    for i, campo in enumerate(CAMPOS_ORDEN, 1):
        print(f"  {i} - {campo}")
    print("  0 - Volver")

    opciones = ["0"] + [str(i) for i in range(1, len(CAMPOS_ORDEN) + 1)]
    opcion = pedir_opcion("  Elige: ", opciones)

    if opcion == "0":
        return vista_actual

    campo_elegido = CAMPOS_ORDEN[int(opcion) - 1]
    orden = pedir_opcion("  Orden: (a)scendente / (d)escendente: ", ["a", "d"])
    desc = orden == "d"

    try:
        resultado = ordenar_por(vista_actual, campo_elegido, desc)
        orden_texto = "descendente" if desc else "ascendente"
        print(f"\n  Ordenado por '{campo_elegido}' ({orden_texto}).")
        return resultado
    except KeyError as e:
        print(f"  Error: {e}")
        return vista_actual


def main():
    print("\n" + "=" * 50)
    print("  DataManager CLI")
    print("  Sistema Informático de Denuncias Policiales (SIDPOL)")
    print("  Lima Metropolitana · 2021-2026")
    print("=" * 50)

    print("\nCargando datos...")
    try:
        datos = cargar_datos(RUTA_CSV)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Filtramos registros con errores antes de trabajar
    datos_limpios, errores = filtrar_validos(datos)
    print(f"  {len(datos_limpios):,} registros cargados.", end="")
    if errores:
        print(f" ({len(errores)} descartados por errores)")
    else:
        print(" (todos válidos)")

    # Copiamos la lista para no perder los datos originales al filtrar
    vista_actual = datos_limpios[:]

    while True:
        print("\n" + "-" * 35)
        print(f"  Registros en pantalla: {len(vista_actual):,}")
        print("-" * 35)
        print("  1 - Mostrar datos")
        print("  2 - Filtrar")
        print("  3 - Ordenar")
        print("  4 - Ver estadísticas")
        print("  5 - Exportar estadísticas a JSON")
        print("  6 - Exportar datos actuales a JSON")
        print("  7 - Resetear (volver a todos los datos)")
        print("  0 - Salir")

        opcion = pedir_opcion("\n  Elige una opción: ", ["0", "1", "2", "3", "4", "5", "6", "7"])

        if opcion == "0":
            print("\n  Hasta luego.\n")
            break

        elif opcion == "1":
            imprimir_tabla(vista_actual)

        elif opcion == "2":
            vista_actual = menu_filtrar(vista_actual)

        elif opcion == "3":
            vista_actual = menu_ordenar(vista_actual)

        elif opcion == "4":
            estadisticas = calcular_estadisticas(vista_actual)
            imprimir_estadisticas(estadisticas)

        elif opcion == "5":
            estadisticas = calcular_estadisticas(vista_actual)
            try:
                exportar_estadisticas(estadisticas, RUTA_ESTADISTICAS)
            except OSError as e:
                print(f"  Error al guardar: {e}")

        elif opcion == "6":
            try:
                exportar_registros(vista_actual, RUTA_RESULTADOS)
            except OSError as e:
                print(f"  Error al guardar: {e}")

        elif opcion == "7":
            # Volvemos a la lista completa sin filtros
            vista_actual = datos_limpios[:]
            print(f"\n  Vista reseteada. {len(vista_actual):,} registros cargados.")


if __name__ == "__main__":
    main()
