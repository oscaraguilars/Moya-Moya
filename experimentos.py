# Mide el tiempo de la versión secuencial y de la paralela con 1, 2 y 4 workers.
# Cada prueba se repite 3 veces y se guarda el promedio en resultados/resumen.csv
import csv
import os
import time

from src.datos import generar_datos
from src.secuencial import procesar_secuencial
from src.paralelo import procesar_paralelo

N = 10_000_000
WORKERS = [1, 2, 4]
REPETICIONES = 3


def medir(funcion, *args):
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        funcion(*args)
        tiempos.append(time.perf_counter() - inicio)
    return sum(tiempos) / REPETICIONES


if __name__ == '__main__':
    datos = generar_datos(N)

    t_secuencial = medir(procesar_secuencial, datos)
    print(f'secuencial: {t_secuencial:.3f} s')

    filas = []
    for w in WORKERS:
        t = medir(procesar_paralelo, datos, w)
        if w == 1:
            t1 = t
        speedup = t1 / t
        eficiencia = speedup / w
        filas.append([w, round(t, 4), round(speedup, 2), round(eficiencia, 2)])
        print(f'{w} workers: {t:.3f} s  speedup {speedup:.2f}  eficiencia {eficiencia:.2f}')

    os.makedirs('resultados', exist_ok=True)
    with open('resultados/resumen.csv', 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['workers', 'tiempo_s', 'speedup', 'eficiencia'])
        escritor.writerows(filas)
        escritor.writerow(['secuencial', round(t_secuencial, 4), '', ''])
