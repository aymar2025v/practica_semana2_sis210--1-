# EXP-AED-002 · Búsqueda lineal vs. binaria — SIS210 Semana 2

## ¿Qué es cada archivo?

| Archivo | Lenguaje | Función |
|---|---|---|
| `src/benchmark.py` | Python | Motor del experimento: corre lineal vs binaria para todos los n, escenarios y repeticiones; mide tiempo y comparaciones; genera los CSV de resultados |
| `src/graficos.py` | Python | Lee el CSV de resumen y dibuja los 2 gráficos obligatorios: n vs. comparaciones, n vs. tiempo |
| `src/benchmark.cpp` | C++20 | El **mismo experimento**, implementado en C++, para poder comparar Python vs C++ (la guía lo exige en la sección 6.6: complejidad teórica vs. velocidad real según el lenguaje) |

La guía pide implementar en **ambos lenguajes** y contrastar los resultados — por eso hay dos motores de experimento equivalentes.

## Estructura de carpetas

```
practica_semana2_sis210/
├── venv/ (.venv)                  # entorno virtual, no se sube a Git
├── .gitignore
├── requirements.txt
├── README.md
├── data/
│   └── Online Retail.xlsx         # dataset real de UCI
├── src/
│   ├── benchmark.py
│   ├── graficos.py
│   └── benchmark.cpp
└── results/
    ├── resultados_crudos.csv       # salida de benchmark.py
    ├── resumen_estadistico.csv     # salida de benchmark.py
    ├── resultados_crudos_cpp.csv   # salida de benchmark.cpp
    ├── n_vs_comparaciones.png      # salida de graficos.py
    └── n_vs_tiempo.png             # salida de graficos.py
```

## 1. Entorno virtual (ya lo tienes activo si ves `(.venv)` en tu prompt)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Ejecutar el experimento en Python

⚠️ En **PowerShell** la continuación de línea es el acento grave `` ` ``, no la barra invertida `\` (esa es de Bash/Linux). O simplemente escribe todo en una sola línea:

```powershell
cd src
python benchmark.py --datos "../data/Online Retail.xlsx" --col CustomerID --salida ../results/resultados_crudos.csv --resumen ../results/resumen_estadistico.csv
```

Si prefieres partirlo en varias líneas en PowerShell:
```powershell
python benchmark.py --datos "../data/Online Retail.xlsx" --col CustomerID `
    --salida ../results/resultados_crudos.csv `
    --resumen ../results/resumen_estadistico.csv
```

Sin `--datos`, el script usa datos sintéticos (útil para probar rápido).

## 3. Generar los gráficos

```powershell
python graficos.py --resumen ../results/resumen_estadistico.csv
```

Genera `n_vs_comparaciones.png` y `n_vs_tiempo.png` en la carpeta actual — muévelos a `results/`.

## 4. Ejecutar el experimento en C++20

Necesitas un compilador de C++ (Windows no trae uno por defecto):

**Opción A — MinGW-w64 vía MSYS2** (recomendada si quieres todo nativo en Windows):
1. Instala MSYS2 desde https://www.msys2.org/
2. En la terminal "MSYS2 MinGW64": `pacman -S mingw-w64-x86_64-gcc`
3. Agrega `C:\msys64\mingw64\bin` al PATH de Windows y reinicia PowerShell
4. Verifica: `g++ --version`

**Opción B — WSL** (si prefieres un entorno Linux dentro de Windows):
```powershell
wsl --install
```
Luego dentro de WSL: `sudo apt install g++`, y compilas ahí en vez de en PowerShell.

Una vez tengas `g++` disponible:

```powershell
cd src
g++ -std=c++20 -O2 -o benchmark.exe benchmark.cpp
.\benchmark.exe
```

Esto genera `resultados_crudos_cpp.csv` — muévelo a `results/`. Por ahora usa datos sintéticos (`generarDatos`); si quieres que también use el dataset real, exporta antes las claves a un `.csv` de una columna desde Python:

```python
import pandas as pd
df = pd.read_excel("data/Online Retail.xlsx")
df["CustomerID"].dropna().astype(int).to_csv("data/customer_ids.csv", index=False, header=False)
```

y agrega una función `cargarDatosDesdeCSV` en `benchmark.cpp` que lea ese archivo con `ifstream` + `getline`.

## 5. Con los resultados de ambos lenguajes, ya puedes comparar

Con `resultados_crudos.csv` (Python) y `resultados_crudos_cpp.csv` (C++) en `results/`, tienes todo para la sección "Complejidad vs. velocidad" del informe: compara tiempos entre lenguajes para el mismo n y algoritmo, y explica que la complejidad teórica (O, Ω, Θ) es la misma en ambos, pero las constantes (intérprete vs. compilado) cambian el tiempo real.

## Pendiente para completar la práctica
- Correr `benchmark.cpp` (aún no lo has hecho).
- Pasar el análisis teórico previo (T(n), O, Ω, Θ) al informe.
- Completar la tabla de indicadores comparando Python vs C++.
- Redactar la discusión de discrepancias teoría/tiempo.
- Commits `baseline`, `analysis`, `benchmark`, `final` en Git.
