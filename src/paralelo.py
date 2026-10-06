import concurrent.futures
from src.secuencial import procesar_secuencial

def _procesar_bloque(bloque: list[float | int]) -> float:
    """Procesa un bloque individual de datos utilizando la función secuencial."""
    return procesar_secuencial(bloque)

def procesar_paralelo(datos: list[float | int], workers: int) -> float:
    """
    Divide los datos en 'workers' bloques y calcula la suma total
    de f(x) ejecutando cada bloque en un proceso independiente.
    """
    if not datos:
        return 0.0
    
    if workers <= 1:
        return procesar_secuencial(datos)

    n = len(datos)
    tamanio_bloque = (n + workers - 1) // workers
    
    bloques = [datos[i:i + tamanio_bloque] for i in range(0, n, tamanio_bloque)]

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        resultados = executor.map(_procesar_bloque, bloques)

    return sum(resultados)
