"""
Experimentos de rendimiento: secuencial vs paralelo.

Corre el procesamiento secuencial y el paralelo con distinta cantidad de workers,
repite cada configuración varias veces y guarda los tiempos en resultados/tiempos.csv.

Uso:
    python experimentos.py
    python experimentos.py --n 10000000 --workers 1 2 4 8 --repeticiones 3
"""
import argparse
import csv
import os
import time

from src.datos import generar_datos
from src.secuencial import procesar_secuencial
from src.paralelo import procesar_paralelo

CARPETA = 'resultados'


def medir(funcion, *args):
    """Ejecuta la función y regresa (tiempo en segundos, resultado)."""
    inicio = time.perf_counter()
    resultado = funcion(*args)
    fin = time.perf_counter()
    return fin - inicio, resultado


def correr_experimentos(n, lista_workers, repeticiones):
    print(f'Generando {n:,} datos...')
    datos = generar_datos(n)

    filas = []

    # Versión secuencial (sin procesos), como referencia
    for prueba in range(1, repeticiones + 1):
        tiempo, suma_secuencial = medir(procesar_secuencial, datos)
        filas.append(['secuencial', 1, prueba, tiempo])
        print(f'secuencial            prueba {prueba}: {tiempo:.3f} s')

    # Versión paralela con cada cantidad de workers
    for workers in lista_workers:
        for prueba in range(1, repeticiones + 1):
            tiempo, suma = medir(procesar_paralelo, datos, workers)
            filas.append(['paralelo', workers, prueba, tiempo])
            print(f'paralelo {workers:2d} workers  prueba {prueba}: {tiempo:.3f} s')

            # El resultado debe ser el mismo que el secuencial
            # (puede variar en los últimos decimales por el orden de las sumas)
            if abs(suma - suma_secuencial) / suma_secuencial > 1e-9:
                print('  ¡Ojo! el resultado no coincide con el secuencial')

    return filas


def guardar_tiempos(filas):
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, 'tiempos.csv')
    with open(ruta, 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['version', 'workers', 'prueba', 'tiempo_s'])
        for version, workers, prueba, tiempo in filas:
            escritor.writerow([version, workers, prueba, round(tiempo, 4)])
    print(f'Tiempos guardados en {ruta}')


def calcular_resumen(filas):
    """
    Calcula el tiempo promedio de cada configuración, el speedup y la eficiencia.

    Speedup:    S_p = T_1 / T_p   (T_1 = tiempo promedio con 1 worker)
    Eficiencia: E_p = S_p / p
    """
    # Agrupar los tiempos por configuración
    tiempos = {}
    for version, workers, prueba, tiempo in filas:
        tiempos.setdefault((version, workers), []).append(tiempo)

    promedios = {clave: sum(lista) / len(lista) for clave, lista in tiempos.items()}
    if ('paralelo', 1) not in promedios:
        raise ValueError('Para calcular el speedup hay que incluir 1 worker en --workers')
    t1 = promedios[('paralelo', 1)]

    resumen = []
    for (version, workers), promedio in promedios.items():
        speedup = t1 / promedio
        eficiencia = speedup / workers
        resumen.append([version, workers] + tiempos[(version, workers)] + [promedio, speedup, eficiencia])
    return resumen


def guardar_resumen(resumen, repeticiones):
    ruta = os.path.join(CARPETA, 'resumen.csv')
    encabezado = ['version', 'workers'] + [f'prueba_{i}' for i in range(1, repeticiones + 1)]
    encabezado += ['promedio_s', 'speedup', 'eficiencia']
    with open(ruta, 'w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezado)
        for fila in resumen:
            escritor.writerow(fila[:2] + [round(valor, 4) for valor in fila[2:]])
    print(f'Resumen guardado en {ruta}')


def mostrar_resumen(resumen):
    print()
    print(f'{"versión":<12}{"workers":>8}{"promedio (s)":>14}{"speedup":>10}{"eficiencia":>12}')
    for fila in resumen:
        version, workers = fila[0], fila[1]
        promedio, speedup, eficiencia = fila[-3], fila[-2], fila[-1]
        print(f'{version:<12}{workers:>8}{promedio:>14.3f}{speedup:>10.2f}{eficiencia:>12.2f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Experimentos secuencial vs paralelo')
    parser.add_argument('--n', type=int, default=10_000_000, help='cantidad de datos')
    parser.add_argument('--workers', type=int, nargs='+', default=[1, 2, 4, 8, 16],
                        help='cantidades de workers a probar')
    parser.add_argument('--repeticiones', type=int, default=3, help='veces que se repite cada configuración')
    args = parser.parse_args()

    filas = correr_experimentos(args.n, args.workers, args.repeticiones)
    guardar_tiempos(filas)

    resumen = calcular_resumen(filas)
    guardar_resumen(resumen, args.repeticiones)
    mostrar_resumen(resumen)
