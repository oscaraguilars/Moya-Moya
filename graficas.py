"""
Gráficas de rendimiento a partir de resultados/resumen.csv.

Genera:
    resultados/tiempo_vs_workers.png
    resultados/speedup_vs_workers.png
    resultados/eficiencia_vs_workers.png

Uso (después de correr experimentos.py):
    python graficas.py
"""
import csv
import os

import matplotlib
matplotlib.use('Agg')  # para guardar las imágenes sin abrir ventanas
import matplotlib.pyplot as plt

CARPETA = 'resultados'


def leer_resumen():
    ruta = os.path.join(CARPETA, 'resumen.csv')
    secuencial = None
    paralelo = []
    with open(ruta) as archivo:
        for fila in csv.DictReader(archivo):
            datos = {
                'workers': int(fila['workers']),
                'promedio': float(fila['promedio_s']),
                'speedup': float(fila['speedup']),
                'eficiencia': float(fila['eficiencia']),
            }
            if fila['version'] == 'secuencial':
                secuencial = datos
            else:
                paralelo.append(datos)
    paralelo.sort(key=lambda d: d['workers'])
    return secuencial, paralelo


def grafica_tiempo(secuencial, paralelo):
    workers = [d['workers'] for d in paralelo]
    tiempos = [d['promedio'] for d in paralelo]

    plt.figure(figsize=(8, 5))
    plt.plot(workers, tiempos, marker='o', label='Paralelo')
    if secuencial:
        plt.axhline(secuencial['promedio'], color='gray', linestyle='--', label='Secuencial')
    for w, t in zip(workers, tiempos):
        plt.annotate(f'{t:.2f} s', (w, t), textcoords='offset points', xytext=(0, 8), ha='center')
    plt.title('Número de workers vs tiempo de ejecución')
    plt.xlabel('Workers')
    plt.ylabel('Tiempo promedio (s)')
    plt.xticks(workers)
    plt.ylim(0, max(tiempos) * 1.15)  # margen arriba para las etiquetas
    plt.grid(alpha=0.3)
    plt.legend()
    guardar('tiempo_vs_workers.png')


def grafica_speedup(paralelo):
    workers = [d['workers'] for d in paralelo]
    speedup = [d['speedup'] for d in paralelo]

    plt.figure(figsize=(8, 5))
    plt.plot(workers, speedup, marker='o', label='Speedup obtenido')
    plt.plot(workers, workers, color='gray', linestyle='--', label='Speedup ideal (S = p)')
    plt.title('Número de workers vs speedup')
    plt.xlabel('Workers')
    plt.ylabel('Speedup (T1 / Tp)')
    plt.xticks(workers)
    plt.grid(alpha=0.3)
    plt.legend()
    guardar('speedup_vs_workers.png')


def grafica_eficiencia(paralelo):
    workers = [d['workers'] for d in paralelo]
    eficiencia = [d['eficiencia'] for d in paralelo]

    plt.figure(figsize=(8, 5))
    plt.plot(workers, eficiencia, marker='o', label='Eficiencia obtenida')
    plt.axhline(1, color='gray', linestyle='--', label='Eficiencia ideal (E = 1)')
    plt.title('Número de workers vs eficiencia')
    plt.xlabel('Workers')
    plt.ylabel('Eficiencia (Sp / p)')
    plt.xticks(workers)
    plt.ylim(0, 1.1)
    plt.grid(alpha=0.3)
    plt.legend()
    guardar('eficiencia_vs_workers.png')


def guardar(nombre):
    ruta = os.path.join(CARPETA, nombre)
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()
    print(f'Gráfica guardada en {ruta}')


if __name__ == '__main__':
    secuencial, paralelo = leer_resumen()
    grafica_tiempo(secuencial, paralelo)
    grafica_speedup(paralelo)
    grafica_eficiencia(paralelo)
