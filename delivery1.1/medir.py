"""Unidad 1: complejidad (Big O) medida en la práctica, no solo dicha en la teoría."""
import random
import time

from algoritmos import busqueda
from algoritmos.ordenamiento import ALGORITMOS
from estructuras.arbol import ABB, AVL


def tiempo(funcion, *args, **kwargs):
    inicio = time.perf_counter()
    funcion(*args, **kwargs)
    return time.perf_counter() - inicio


def tabla_ordenamiento(tamanios=(250, 500, 1000), semilla=1):
    """Devuelve {algoritmo: [segundos por cada tamaño]}. Al duplicar n, los O(n^2)
    tardan ~4 veces más y los O(n log n) algo más del doble."""
    azar = random.Random(semilla)
    resultado = {nombre: [] for nombre in ALGORITMOS}
    for n in tamanios:
        datos = [azar.randint(0, 10 ** 6) for _ in range(n)]
        for nombre, funcion in ALGORITMOS.items():
            resultado[nombre].append(tiempo(funcion, datos))
    return tamanios, resultado


def comparar_busquedas(n=100_000, repeticiones=200, semilla=1):
    """Tiempo promedio (en microsegundos) de buscar el último elemento."""
    lista = list(range(n))
    seq = tiempo(lambda: [busqueda.secuencial(lista, n - 1) for _ in range(repeticiones)])
    bin_ = tiempo(lambda: [busqueda.binaria(lista, n - 1) for _ in range(repeticiones)])
    return n, seq / repeticiones * 1e6, bin_ / repeticiones * 1e6


def comparar_arboles(n=500):
    """Inserta claves ya ordenadas: el ABB se vuelve una lista; el AVL se equilibra."""
    abb, avl = ABB(), AVL()
    for clave in range(n):
        abb.insertar(clave)
        avl.insertar(clave)
    return n, abb.altura(), avl.altura(), avl.rotaciones
