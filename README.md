# DataManager CLI — Análisis de Denuncias Policiales en Lima Metropolitana


- **Curso**: Introducción a la Programación en Python y PyTorch
- **Programa**: Pre-Maestría MSc. Ingeniería Estadística
- **Docente**: Jorge Guevara
- **Integrante**: Braulio Arteaga
- **Fecha**: Marzo 2026 
---

## 1. Descripción
 
Aplicación de línea de comandos (CLI) para el procesamiento y análisis descriptivo de denuncias policiales registradas en Lima Metropolitana durante el periodo 2021–2026, utilizando datos del [Sistema Informático de Denuncias Policiales (SIDPOL)](https://observatorio.mininter.gob.pe/proyectos/base-de-datos-hechos-delictivos-basados-en-denuncias-en-el-sidpol) de la Policía Nacional del Perú. 

El proyecto, mediante una arquitectura funcional y reproducible, integra los módulos dictados en enl curso, lo cual incluye desde la gestión de archivos hasta la implementación de pruebas unitarias.


<p align="center">
  <img src="img/denuncia.jpg" width="600" alt="SIDPOL PNP">
  <br>
  <em>Procesamiento de denuncias del SIDPOL</em>
</p>

## 2. Estructura del proyecto

```
datamanager/
├── main.py           # Menú CLI principal (punto de entrada)
├── data_loader.py    # Carga y parseo del CSV
├── validator.py      # Validación de registros
├── processor.py      # Filtros, ordenamiento y estadísticas
├── exporter.py       # Exportación a JSON
├── utils.py          # Funciones auxiliares de UI
├── tests/
│   ├── __init__.py
│   └── test_processor.py  # Suite de pruebas (31 tests)
└── data/
    ├── denuncias_lima.csv  # Dataset principal
    ├── estadisticas.json   # Generado al exportar
    └── resultados.json     # Generado al exportar
```

---

## 3. Requisitos

- Python 3.10 o superior
- pytest (para ejecutar los tests)

```bash
pip install pytest
```

---

## 4. Ejecución

```bash
cd datamanager
python main.py
```

### 4.1. Menú principal

```
DataManager CLI — Denuncias Lima Metropolitana
Fuente: SIDPOL · Período: 2021–2026

  1 - Mostrar datos
  2 - Filtrar
  3 - Ordenar
  4 - Estadísticas
  5 - Exportar estadísticas (JSON)
  6 - Exportar datos actuales (JSON)
  7 - Resetear vista
  0 - Salir
```

### 4.2 Ejemplo de uso

```
# Cargar el programa
python main.py

# Desde el menú:
# 2 → Filtrar → 1 (Modalidad) → 2 (Extorsión)
# 3 → Ordenar → 5 (n_denuncias) → d (descendente)
# 4 → Ver estadísticas del filtro aplicado
# 5 → Exportar estadísticas a data/estadisticas.json
```

---

## 5. Tests

```bash
cd datamanager
pip install pytest
pytest tests/test_processor.py -v
```

Los test realizan lo siguiente:
- Filtros por modalidad, año, distrito y mínimo de denuncias
- Ordenamiento ascendente/descendente y detección de campos inválidos
- Estadísticas con lista vacía, valores normales y casos extremos
- Validación de registros (distrito vacío, modalidad inválida, año fuera de rango, denuncias negativas)

---


## 6. Ejemplo de salida JSON 

```json
{
  "total_registros": 13710,
  "total_denuncias": 1021243,
  "promedio_denuncias": 74.49,
  "max_denuncias": 4706,
  "min_denuncias": 1,
  "por_modalidad": {
    "Extorsión": 39293,
    "Robo": 234109,
    "Hurto": 380739,
    "Estafa": 67145,
    "Homicidio": 3961,
    "Otros": 295996
  },
  "por_anio": {
    "2021": 134026,
    "2022": 178964,
    "2023": 250659,
    "2024": 239447,
    "2025": 203739,
    "2026": 14408
  },
  "top5_distritos": {
    "SAN JUAN DE LURIGANCHO": 105964,
    "LIMA": 104284,
    "SAN MARTIN DE PORRES": 54705,
    "COMAS": 54192,
    "ATE": 47639
  }
}
```
