"""
tests/test_processor.py
Pruebas para verificar que las funciones principales funcionan bien.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from processor import filtrar_por_modalidad, filtrar_por_anio, calcular_estadisticas
from validator import validar_registro


REGISTROS_PRUEBA = [
    {"anio": 2021, "mes": 1, "departamento": "LIMA METROPOLITANA", "provincia": "LIMA",
     "distrito": "MIRAFLORES", "ubigeo": "150122", "modalidad": "Robo", "n_denuncias": 50, "dist_emergencia": 1},
    {"anio": 2022, "mes": 3, "departamento": "LIMA METROPOLITANA", "provincia": "LIMA",
     "distrito": "SAN ISIDRO", "ubigeo": "150131", "modalidad": "Extorsión", "n_denuncias": 10, "dist_emergencia": 1},
    {"anio": 2021, "mes": 2, "departamento": "LIMA METROPOLITANA", "provincia": "LIMA",
     "distrito": "SURQUILLO", "ubigeo": "150140", "modalidad": "Robo", "n_denuncias": 5, "dist_emergencia": 1},
]


def test_filtrar_modalidad():
    resultado = filtrar_por_modalidad(REGISTROS_PRUEBA, "Robo")
    assert len(resultado) == 2


def test_filtrar_modalidad_sin_resultados():
    resultado = filtrar_por_modalidad(REGISTROS_PRUEBA, "Homicidio")
    assert resultado == []


def test_filtrar_anio():
    resultado = filtrar_por_anio(REGISTROS_PRUEBA, 2021)
    assert len(resultado) == 2


def test_estadisticas_valores_normales():
    stats = calcular_estadisticas(REGISTROS_PRUEBA)
    assert stats["total_registros"] == 3
    assert stats["total_denuncias"] == 65
    assert stats["max_denuncias"] == 50
    assert stats["min_denuncias"] == 5


def test_estadisticas_lista_vacia():
    stats = calcular_estadisticas([])
    assert stats["total_registros"] == 0
    assert stats["total_denuncias"] == 0


def test_validar_registro_correcto():
    registro = {
        "anio": 2022, "mes": 5, "departamento": "LIMA METROPOLITANA",
        "provincia": "LIMA", "distrito": "MIRAFLORES", "ubigeo": "150122",
        "modalidad": "Robo", "n_denuncias": 25, "dist_emergencia": 1
    }
    es_valido, mensaje = validar_registro(registro)
    assert es_valido is True


def test_validar_modalidad_invalida():
    registro = {
        "anio": 2022, "mes": 5, "departamento": "LIMA METROPOLITANA",
        "provincia": "LIMA", "distrito": "MIRAFLORES", "ubigeo": "150122",
        "modalidad": "Secuestro", "n_denuncias": 25, "dist_emergencia": 1
    }
    es_valido, _ = validar_registro(registro)
    assert es_valido is False


def test_validar_distrito_vacio():
    registro = {
        "anio": 2022, "mes": 5, "departamento": "LIMA METROPOLITANA",
        "provincia": "LIMA", "distrito": "", "ubigeo": "150122",
        "modalidad": "Robo", "n_denuncias": 25, "dist_emergencia": 1
    }
    es_valido, _ = validar_registro(registro)
    assert es_valido is False
