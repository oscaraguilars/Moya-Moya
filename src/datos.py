import random

def generar_datos(n, semilla=42):
    random.seed(semilla)
    return [random.uniform(1, 1000) for _ in range(n)]
