
### Análisis y Preguntas Teóricas (Parte 2)

#### 4. ¿Por qué el problema seleccionado puede paralelizarse?
El problema es **completamente independiente (Embarrassingly Parallel)**. La función $f(x)$ se calcula individualmente para cada número $x_i$ dentro del arreglo, sin depender de iteraciones previas o posteriores ni requerir estados compartidos en memoria. Esto permite dividir la lista de datos en $N$ bloques independientes, procesar cada bloque simultáneamente en un núcleo de CPU distinto y reducir las sumas parciales en una suma global final.

#### 5. ¿En qué momento agregar más workers deja de ser beneficioso?
Agregar más *workers* deja de ser beneficioso cuando:
1. **Límite de núcleos físicos:** El número de *workers* excede la cantidad de hilos/núcleos lógicos del procesador, lo que provoca competencia por CPU y sobrecarga por cambios de contexto (*context switching*).
2. **Sobrecarga de comunicación e IPC (Ley de Amdahl):** La creación de procesos con `ProcessPoolExecutor` requiere la serialización de datos (*pickling*) y la clonación del intérprete de Python. Cuando el costo de transferir y sincronizar los bloques supera el tiempo de cálculo real, el rendimiento se estanca o empeora.

#### 6. ¿Qué limitaciones tiene el hardware utilizado?
- **Número limitado de núcleos lógicos/físicos** en el procesador de ejecución.
- **Ancho de banda de memoria RAM (Memory Bottleneck):** Múltiples procesos leyendo arreglos grandes en paralelo saturan el bus de datos de la memoria.
- **Aislamiento de memoria:** Python crea espacios de memoria independientes por cada proceso hijo, lo que incrementa el uso total de memoria RAM por duplicación de buffers.

#### 7. ¿Este experimento representa HPC o solamente demuestra principios utilizados en HPC? Justifiquen.
**Demuestra principios fundamentales de HPC** (como descomposición de dominio/datos, modelo *fork-join*, aceleración por multinúcleo y análisis de Ley de Amdahl), pero **no es un entorno de HPC real en producción**. 

Un sistema de HPC verdadero involucra arquitecturas multinodo distribuidas con interconexiones de baja latencia (InfiniBand), bibliotecas de paso de mensajes entre nodos (MPI), aceleradores de hardware (GPUs/TPUs) y gestores de cola (Slurm), mientras que este proyecto realiza paralelización local en una sola computadora personal.
