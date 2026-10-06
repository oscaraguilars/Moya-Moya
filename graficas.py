# Hace las gráficas de tiempo, speedup y eficiencia con los datos de resultados/resumen.csv
# Primero hay que correr experimentos.py
import csv

import matplotlib.pyplot as plt

workers, tiempos, speedup, eficiencia = [], [], [], []
with open('resultados/resumen.csv') as archivo:
    for fila in csv.DictReader(archivo):
        if fila['workers'] == 'secuencial':
            continue
        workers.append(int(fila['workers']))
        tiempos.append(float(fila['tiempo_s']))
        speedup.append(float(fila['speedup']))
        eficiencia.append(float(fila['eficiencia']))


def grafica(y, titulo, etiqueta_y, archivo, ideal):
    plt.figure()
    plt.plot(workers, y, marker='o', label='Obtenido')
    if ideal:
        plt.plot(workers, ideal, linestyle='--', color='gray', label='Ideal')
        plt.legend()
    plt.title(titulo)
    plt.xlabel('Workers')
    plt.ylabel(etiqueta_y)
    plt.xticks(workers)
    plt.grid(alpha=0.3)
    plt.savefig(f'resultados/{archivo}')
    plt.close()


grafica(tiempos, 'Workers vs tiempo', 'Tiempo (s)', 'tiempo.png', None)
grafica(speedup, 'Workers vs speedup', 'Speedup', 'speedup.png', workers)
grafica(eficiencia, 'Workers vs eficiencia', 'Eficiencia', 'eficiencia.png', [1] * len(workers))
