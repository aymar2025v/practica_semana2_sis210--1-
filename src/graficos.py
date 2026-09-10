"""
Genera los dos gráficos mínimos que pide la guía:
  - n vs. comparaciones (mediana)
  - n vs. tiempo (mediana)
Usa el CSV de resumen producido por benchmark.py.

Uso:
    python graficos.py --resumen resumen_estadistico.csv
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt


def graficar(resumen_csv):
    df = pd.read_csv(resumen_csv)

    fig1, ax1 = plt.subplots()
    for algoritmo, grupo in df.groupby("algoritmo"):
        grupo = grupo.sort_values("n")
        ax1.plot(grupo["n"], grupo["comparaciones_mediana"], marker="o", label=algoritmo)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("n (tamaño de entrada)")
    ax1.set_ylabel("Comparaciones (mediana)")
    ax1.set_title("n vs. comparaciones")
    ax1.legend()
    fig1.savefig("n_vs_comparaciones.png", dpi=150, bbox_inches="tight")

    fig2, ax2 = plt.subplots()
    for algoritmo, grupo in df.groupby("algoritmo"):
        grupo = grupo.sort_values("n")
        ax2.plot(grupo["n"], grupo["tiempo_mediana_ns"], marker="o", label=algoritmo)
    ax2.set_xscale("log")
    ax2.set_xlabel("n (tamaño de entrada)")
    ax2.set_ylabel("Tiempo (ns, mediana)")
    ax2.set_title("n vs. tiempo")
    ax2.legend()
    fig2.savefig("n_vs_tiempo.png", dpi=150, bbox_inches="tight")

    print("Gráficos guardados: n_vs_comparaciones.png, n_vs_tiempo.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resumen", type=str, default="resumen_estadistico.csv")
    args = parser.parse_args()
    graficar(args.resumen)
