from src.operacion import f

def procesar_secuencial(datos):
    suma_total = 0.0
    for x in datos:
        suma_total += f(x)
    return suma_total
