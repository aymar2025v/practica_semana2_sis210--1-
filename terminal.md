
```bash
PS C:\Users\ASUS\Downloads\practica_semana2_sis210 (1)> (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& "c:\Users\ASUS\Downloads\practica_semana2_sis210 (1)\.venv\Scripts\Activate.ps1")
(.venv) PS C:\Users\ASUS\Downloads\practica_semana2_sis210 (1)> cd src
(.venv) PS C:\Users\ASUS\Downloads\practica_semana2_sis210 (1)\src> python benchmark.py --datos "../data/Online Retail.xlsx" --col CustomerID --salida ../results/resultados_crudos.csv --resumen ../results/resumen_estadistico.csv
n=    100  listo  (orden: 25,500 ns)
n=   1000  listo  (orden: 307,200 ns)
n=  10000  listo  (orden: 2,943,200 ns)
n= 100000  listo  (orden: 1,456,800 ns)
n= 500000  listo  (orden: 1,542,700 ns)

CSV guardado en: ../results/resultados_crudos.csv  (1200 filas)
Resumen guardado en: ../results/resumen_estadistico.csv
  algoritmo       n  comparaciones_prom  comparaciones_mediana  tiempo_prom_ns  tiempo_mediana_ns  tiempo_min_ns  tiempo_max_ns
0   binaria     100                 6.5                    6.5     2060.833333             1900.0           1500          11300
1   binaria    1000                 9.5                    9.5     3245.833333             3100.0           2500           7300
2   binaria   10000                12.5                   12.5     5812.500000             4850.0           3600          15400
3   binaria  100000                12.5                   12.5     4622.500000             4000.0           3200          16400
4   binaria  500000                12.5                   12.5     7520.000000             4800.0           3500         125400
5    lineal     100                63.0                   75.5     6579.166667             8650.0            500          20300
6    lineal    1000               625.5                  750.5    76995.833333           105200.0            700         412300
7    lineal   10000              2733.0                 3279.5   564863.333333           497050.0            800       13917200
8    lineal  100000              2733.0                 3279.5   572477.500000           404400.0            500       18859100
9    lineal  500000              2733.0                 3279.5   543217.500000           494850.0            700        7471000
(.venv) PS C:\Users\ASUS\Downloads\practica_semana2_sis210 (1)\src> python graficos.py --resumen ../results/resumen_estadistico.csv
Gráficos guardados: n_vs_comparaciones.png, n_vs_tiempo.png
(.venv) PS C:\Users\ASUS\Downloads\practica_semana2_sis210 (1)\src> g++ -std=c++20 -O2 -o benchmark.exe benchmark.cpp
(.venv) PS C:\Users\ASUS\Downloads\practica_semana2_sis210 (1)\src> ./benchmark.exe        
n=100 listo (orden: 10500 ns)
n=1000 listo (orden: 117900 ns)
n=10000 listo (orden: 1224000 ns)
n=100000 listo (orden: 18660500 ns)
n=500000 listo (orden: 83787000 ns)

CSV guardado en: resultados_crudos_cpp.csv (1200 filas)
(.venv) PS C:\Users\ASUS\Downloads\practica_semana2_sis210 (1)\src> 
```

## hola xd

