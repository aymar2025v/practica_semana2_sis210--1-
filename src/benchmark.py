"""
SIS210 - Algoritmos y Estructuras de Datos - Semana 2
EXP-AED-002: Búsqueda lineal vs. búsqueda binaria
Autor: Aymar (completar datos)

Este script:
  1. Carga (o genera) una muestra de claves tipo CustomerID.
  2. Corre la matriz n x algoritmo x escenario x repeticiones.
  3. Cuenta operaciones y mide tiempo con perf_counter_ns().
  4. Separa el tiempo de ordenamiento (para binaria) del tiempo de búsqueda.
  5. Guarda un CSV con los datos crudos.

Uso:
    python benchmark.py                     -> usa datos sintéticos
    python benchmark.py --csv ruta.csv --col CustomerID   -> usa el dataset UCI Online Retail
"""

import argparse
import csv
import random
from pathlib import Path
from time import perf_counter_ns

import pandas as pd

# --------------------------------------------------------------------------
# 1. Algoritmos instrumentados (contador de operaciones incluido)
# --------------------------------------------------------------------------

def busqueda_lineal(a, x):
    """Recorre a de izquierda a derecha. Cuenta cada comparación."""
    ops = 0
    for i, valor in enumerate(a):
        ops += 1
        if valor == x:
            return i, ops
    return -1, ops


def busqueda_binaria(a, x):
    """Requiere que 'a' esté ordenado. Cuenta cada comparación de pivote."""
    izq, der, ops = 0, len(a) - 1, 0
    while izq <= der:
        medio = izq + (der - izq) // 2
        ops += 1
        if a[medio] == x:
            return medio, ops
        if a[medio] < x:
            izq = medio + 1
        else:
            der = medio - 1
    return -1, ops


# --------------------------------------------------------------------------
# 2. Preparación de datos
# --------------------------------------------------------------------------

def generar_datos_sinteticos(n, semilla=42):
    """Genera n claves enteras únicas, simulando CustomerID.
    Reemplaza esta función por cargar_datos_reales() cuando tengas el CSV
    de Online Retail (UCI, DOI 10.24432/C5BW33)."""
    rng = random.Random(semilla)
    # Rango amplio para evitar colisiones al muestrear sin reemplazo
    universo = range(10_000, 10_000 + n * 10)
    return rng.sample(universo, n)


def cargar_datos_reales(ruta_archivo, columna="CustomerID", n=None, semilla=42):
    """Carga claves reales desde el dataset Online Retail (UCI).
    Descarga: https://archive.ics.uci.edu/dataset/352/online+retail
    (el archivo oficial es 'Online Retail.xlsx'; también acepta .csv si ya
    lo convertiste tú mismo, p.ej. con pandas o Excel -> Guardar como CSV).
    """
    ruta = Path(ruta_archivo)
    if ruta.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(ruta)  # requiere: pip install openpyxl
    else:
        df = pd.read_csv(ruta, encoding="ISO-8859-1")

    claves = df[columna].dropna().astype(int).unique().tolist()
    if n is not None:
        rng = random.Random(semilla)
        claves = rng.sample(claves, min(n, len(claves)))
    return claves


def elegir_objetivo(datos, escenario, presente=True):
    """Devuelve la clave objetivo según el escenario pedido por la guía:
    inicio, centro, final, ausente. 'datos' debe estar en el orden que
    usa el algoritmo (original para lineal, ordenado para binaria)."""
    if escenario == "ausente" or not presente:
        # Un valor que casi seguro no está en la muestra
        return max(datos) + 999_999
    if escenario == "inicio":
        return datos[0]
    if escenario == "centro":
        return datos[len(datos) // 2]
    if escenario == "final":
        return datos[-1]
    raise ValueError(f"Escenario desconocido: {escenario}")


# --------------------------------------------------------------------------
# 3. Motor del experimento
# --------------------------------------------------------------------------

TAMANOS = [100, 1_000, 10_000, 100_000, 500_000]
ESCENARIOS = ["inicio", "centro", "final", "ausente"]
REPETICIONES = 30


def correr_experimento(muestra_por_n, salida_csv):
    """muestra_por_n: dict {n: lista_de_claves_de_tamano_n}"""
    filas = []

    for n in TAMANOS:
        if n not in muestra_por_n:
            continue
        datos_originales = list(muestra_por_n[n])  # orden de llegada (para lineal)

        # --- Tiempo de ordenamiento (se reporta aparte, no se mezcla) ---
        t0 = perf_counter_ns()
        datos_ordenados = sorted(datos_originales)  # para binaria
        t1 = perf_counter_ns()
        tiempo_orden_ns = t1 - t0

        for escenario in ESCENARIOS:
            objetivo_lineal = elegir_objetivo(datos_originales, escenario)
            objetivo_binaria = elegir_objetivo(datos_ordenados, escenario)

            for rep in range(REPETICIONES):
                # ---- Lineal ----
                inicio = perf_counter_ns()
                _, ops_lineal = busqueda_lineal(datos_originales, objetivo_lineal)
                fin = perf_counter_ns()
                filas.append({
                    "algoritmo": "lineal",
                    "n": n,
                    "escenario": escenario,
                    "repeticion": rep,
                    "comparaciones": ops_lineal,
                    "tiempo_ns": fin - inicio,
                    "tiempo_orden_ns": 0,  # no aplica
                })

                # ---- Binaria ----
                inicio = perf_counter_ns()
                _, ops_binaria = busqueda_binaria(datos_ordenados, objetivo_binaria)
                fin = perf_counter_ns()
                filas.append({
                    "algoritmo": "binaria",
                    "n": n,
                    "escenario": escenario,
                    "repeticion": rep,
                    "comparaciones": ops_binaria,
                    "tiempo_ns": fin - inicio,
                    "tiempo_orden_ns": tiempo_orden_ns,  # reportado una vez por n
                })

        print(f"n={n:>7}  listo  (orden: {tiempo_orden_ns:,} ns)")

    df = pd.DataFrame(filas)
    df.to_csv(salida_csv, index=False)
    print(f"\nCSV guardado en: {salida_csv}  ({len(df)} filas)")
    return df


# --------------------------------------------------------------------------
# 4. Resumen estadístico (promedio, mediana, min, max)
# --------------------------------------------------------------------------

def resumen(df):
    agg = df.groupby(["algoritmo", "n"]).agg(
        comparaciones_prom=("comparaciones", "mean"),
        comparaciones_mediana=("comparaciones", "median"),
        tiempo_prom_ns=("tiempo_ns", "mean"),
        tiempo_mediana_ns=("tiempo_ns", "median"),
        tiempo_min_ns=("tiempo_ns", "min"),
        tiempo_max_ns=("tiempo_ns", "max"),
    ).reset_index()
    return agg


# --------------------------------------------------------------------------
# 5. Punto de entrada
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="EXP-AED-002: lineal vs binaria")
    parser.add_argument("--datos", type=str, default=None,
                         help="Ruta al archivo real de Online Retail (.xlsx o .csv). "
                              "Si se omite, usa datos sintéticos.")
    parser.add_argument("--col", type=str, default="CustomerID",
                         help="Columna a usar como clave (CustomerID o StockCode).")
    parser.add_argument("--salida", type=str, default="resultados_crudos.csv")
    parser.add_argument("--resumen", type=str, default="resumen_estadistico.csv")
    args = parser.parse_args()

    muestra_por_n = {}
    for n in TAMANOS:
        if args.datos:
            muestra_por_n[n] = cargar_datos_reales(args.datos, args.col, n=n)
        else:
            muestra_por_n[n] = generar_datos_sinteticos(n)

    df = correr_experimento(muestra_por_n, args.salida)
    agg = resumen(df)
    agg.to_csv(args.resumen, index=False)
    print(f"Resumen guardado en: {args.resumen}")
    print(agg)


if __name__ == "__main__":
    main()
