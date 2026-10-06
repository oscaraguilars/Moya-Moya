from src.datos import generar_datos
from src.secuencial import procesar_secuencial
from src.paralelo import procesar_paralelo

def probar_paralelo_vs_secuencial():
    datos = generar_datos(100_000, semilla=42)
    resultado_secuencial = procesar_secuencial(datos)
    
    print(f"Resultado Secuencial: {resultado_secuencial:.6f}\n")
    
    for workers in [1, 2, 4, 8]:
        resultado_paralelo = procesar_paralelo(datos, workers=workers)
        diferencia_relativa = abs(resultado_secuencial - resultado_paralelo) / resultado_secuencial
        
        assert diferencia_relativa < 1e-9, (
            f"Fallo de precisión con {workers} workers: "
            f"secuencial={resultado_secuencial}, paralelo={resultado_paralelo}"
        )
        print(f"✓ Test con {workers} worker(s) exitoso (Dif. relativa: {diferencia_relativa:.2e})")

if __name__ == "__main__":
    probar_paralelo_vs_secuencial()
