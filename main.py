import time
from src.datos import generar_datos
from src.secuencial import procesar_secuencial

def main():
    n = 1_000_000
    print(f"Generando {n:,} datos...")
    datos = generar_datos(n)

    print("Ejecutando procesamiento secuencial...")
    inicio = time.perf_counter()
    resultado = procesar_secuencial(datos)
    fin = time.perf_counter()

    tiempo_ejecucion = fin - inicio
    print(f"Suma total: {resultado:.6f}")
    print(f"Tiempo de ejecución secuencial: {tiempo_ejecucion:.4f} segundos")

if __name__ == "__main__":
    main()
