"""
utils.py
Funciones para mostrar datos en pantalla y pedir datos al usuario.
"""


def imprimir_tabla(lista_registros, max_filas=20):
    if not lista_registros:
        print("  (sin resultados)")
        return

    # Cabecera de la tabla
    print(f"\n  {'AÑO':<6} {'MES':<5} {'DISTRITO':<22} {'MODALIDAD':<14} {'DENUNCIAS':>10}")
    print("  " + "-" * 60)

    # Mostramos fila por fila hasta el límite
    for registro in lista_registros[:max_filas]:
        print(
            f"  {registro['anio']:<6} {registro['mes']:<5} {registro['distrito']:<22} "
            f"{registro['modalidad']:<14} {registro['n_denuncias']:>10}"
        )

    # Avisamos si hay más filas que no se muestran
    if len(lista_registros) > max_filas:
        filas_ocultas = len(lista_registros) - max_filas
        print(f"  ... ({filas_ocultas} filas más no mostradas)")

    print(f"\n  Total: {len(lista_registros)} registros\n")


def imprimir_estadisticas(stats):
    print("\n  -- Estadísticas generales --")
    print(f"  Total registros    : {stats['total_registros']:,}")
    print(f"  Total denuncias    : {stats['total_denuncias']:,}")
    print(f"  Promedio x registro: {stats['promedio_denuncias']:,.2f}")
    print(f"  Máximo denuncias   : {stats['max_denuncias']:,}")
    print(f"  Mínimo denuncias   : {stats['min_denuncias']:,}")

    print("\n  -- Por modalidad --")
    for modalidad, total in sorted(stats["por_modalidad"].items(), key=lambda x: x[1], reverse=True):
        print(f"  {modalidad:<14}: {total:>8,}")

    print("\n  -- Por año --")
    for anio, total in stats["por_anio"].items():
        print(f"  {anio}: {total:>8,}")

    print("\n  -- Top 5 distritos --")
    for distrito, total in stats["top5_distritos"].items():
        print(f"  {distrito:<22}: {total:>8,}")

    print()


def pedir_opcion(mensaje, opciones_validas):
    # Repetimos la pregunta hasta que el usuario elija una opción válida
    while True:
        entrada = input(mensaje).strip()
        if entrada in opciones_validas:
            return entrada
        print(f"  Opción no válida. Elige entre: {', '.join(opciones_validas)}")


def pedir_entero(mensaje, minimo=None, maximo=None):
    # Repetimos la pregunta hasta que el usuario ingrese un número válido
    while True:
        try:
            numero = int(input(mensaje).strip())

            if minimo is not None and numero < minimo:
                print(f"  El número debe ser al menos {minimo}.")
                continue

            if maximo is not None and numero > maximo:
                print(f"  El número debe ser como máximo {maximo}.")
                continue

            return numero

        except ValueError:
            print("  Eso no es un número. Intenta de nuevo.")
