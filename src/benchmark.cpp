// SIS210 - Algoritmos y Estructuras de Datos - Semana 2
// EXP-AED-002: Búsqueda lineal vs. búsqueda binaria (C++20)
// Compilar:  g++ -std=c++20 -O2 -o benchmark benchmark.cpp
// Ejecutar:  ./benchmark

#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

using namespace std;
using namespace std::chrono;

// ---------------------------------------------------------------------
// 1. Algoritmos instrumentados
// ---------------------------------------------------------------------

int busquedaLineal(const vector<long long>& a, long long x, long long& ops) {
    ops = 0;
    for (size_t i = 0; i < a.size(); ++i) {
        ++ops;
        if (a[i] == x) return static_cast<int>(i);
    }
    return -1;
}

int busquedaBinaria(const vector<long long>& a, long long x, long long& ops) {
    int izq = 0, der = static_cast<int>(a.size()) - 1;
    ops = 0;
    while (izq <= der) {
        int medio = izq + (der - izq) / 2;
        ++ops;
        if (a[medio] == x) return medio;
        if (a[medio] < x) izq = medio + 1;
        else der = medio - 1;
    }
    return -1;
}

// ---------------------------------------------------------------------
// 2. Preparación de datos (sintéticos; reemplazar por lectura del CSV
//    real de Online Retail si se desea trabajar con el dataset UCI)
// ---------------------------------------------------------------------

vector<long long> generarDatos(int n, unsigned semilla = 42) {
    vector<long long> universo(n * 10);
    for (int i = 0; i < n * 10; ++i) universo[i] = 10000 + i;

    mt19937 rng(semilla);
    shuffle(universo.begin(), universo.end(), rng);
    universo.resize(n);
    return universo;
}

long long elegirObjetivo(const vector<long long>& datos, const string& escenario) {
    if (escenario == "ausente") {
        return *max_element(datos.begin(), datos.end()) + 999999;
    } else if (escenario == "inicio") {
        return datos.front();
    } else if (escenario == "centro") {
        return datos[datos.size() / 2];
    } else if (escenario == "final") {
        return datos.back();
    }
    throw invalid_argument("Escenario desconocido: " + escenario);
}

// ---------------------------------------------------------------------
// 3. Motor del experimento
// ---------------------------------------------------------------------

struct Fila {
    string algoritmo;
    int n;
    string escenario;
    int repeticion;
    long long comparaciones;
    long long tiempo_ns;
    long long tiempo_orden_ns;
};

int main() {
    const vector<int> tamanos = {100, 1000, 10000, 100000, 500000};
    const vector<string> escenarios = {"inicio", "centro", "final", "ausente"};
    const int repeticiones = 30;

    vector<Fila> filas;
    filas.reserve(tamanos.size() * escenarios.size() * repeticiones * 2);

    for (int n : tamanos) {
        vector<long long> datosOriginales = generarDatos(n);

        // --- Tiempo de ordenamiento (se reporta aparte) ---
        vector<long long> datosOrdenados = datosOriginales;
        auto t0 = steady_clock::now();
        sort(datosOrdenados.begin(), datosOrdenados.end());
        auto t1 = steady_clock::now();
        long long tiempoOrdenNs = duration_cast<nanoseconds>(t1 - t0).count();

        for (const auto& escenario : escenarios) {
            long long objetivoLineal = elegirObjetivo(datosOriginales, escenario);
            long long objetivoBinaria = elegirObjetivo(datosOrdenados, escenario);

            for (int rep = 0; rep < repeticiones; ++rep) {
                long long ops;

                // ---- Lineal ----
                auto inicio = steady_clock::now();
                busquedaLineal(datosOriginales, objetivoLineal, ops);
                auto fin = steady_clock::now();
                filas.push_back({"lineal", n, escenario, rep, ops,
                                  duration_cast<nanoseconds>(fin - inicio).count(), 0});

                // ---- Binaria ----
                inicio = steady_clock::now();
                busquedaBinaria(datosOrdenados, objetivoBinaria, ops);
                fin = steady_clock::now();
                filas.push_back({"binaria", n, escenario, rep, ops,
                                  duration_cast<nanoseconds>(fin - inicio).count(),
                                  tiempoOrdenNs});
            }
        }
        cout << "n=" << n << " listo (orden: " << tiempoOrdenNs << " ns)\n";
    }

    // ---------------------------------------------------------------
    // 4. Guardar CSV con datos crudos
    // ---------------------------------------------------------------
    ofstream out("resultados_crudos_cpp.csv");
    out << "algoritmo,n,escenario,repeticion,comparaciones,tiempo_ns,tiempo_orden_ns\n";
    for (const auto& f : filas) {
        out << f.algoritmo << "," << f.n << "," << f.escenario << "," << f.repeticion
            << "," << f.comparaciones << "," << f.tiempo_ns << "," << f.tiempo_orden_ns
            << "\n";
    }
    out.close();

    cout << "\nCSV guardado en: resultados_crudos_cpp.csv (" << filas.size() << " filas)\n";
    return 0;
}
