# Proyecto HPC - Procesamiento Paralelo y Secuencial

Este proyecto compara el rendimiento de la ejecución de una función matemática intensiva de forma secuencial frente a una implementación paralela usando concurrent.futures.

## Requisitos
- Python 3.11 o superior
- Módulos de la librería estándar (math, random, time, concurrent.futures)

## Estructura del Proyecto
- src/operacion.py: Define la función matemática f(x).
- src/datos.py: Genera un conjunto de datos aleatorios con semilla fija.
- src/secuencial.py: Módulo de procesamiento secuencial.
- main.py: Punto de entrada para probar la versión secuencial y medir tiempos.

## Cómo ejecutarlo
python3 main.py

## Investigación: GitFlow
GitFlow es un modelo de administración de ramas diseñado para organizar el desarrollo de software en equipo mediante ramas especializadas:
- main: Código estable listo para producción.
- develop: Rama principal de integración para todas las funcionalidades terminadas.
- feature/...: Ramas independientes donde cada desarrollador crea características aisladas antes de integrarlas mediante un Pull Request.
- release/... y hotfix/...: Preparación de versiones y correcciones rápidas de errores.
