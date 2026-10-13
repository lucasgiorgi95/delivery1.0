"""Unidad 5: algoritmos de ordenamiento. Todos devuelven una lista nueva (no modifican la
original) y aceptan clave=función para ordenar objetos (por ejemplo, por precio).

Complejidad (n = cantidad de elementos):
  burbuja, selección, inserción: O(n^2)  (inserción y burbuja con corte: O(n) si ya está ordenada)
  shell: entre O(n log n) y O(n^2) según la secuencia de saltos
  quicksort: O(n log n) en promedio, O(n^2) en el peor caso
  mergesort: O(n log n) siempre, estable, usa O(n) de memoria extra"""


def _identidad(x):
    return x


def burbuja(lista, clave=None):
    k = clave or _identidad
    a = list(lista)
    n = len(a)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):
            if k(a[j]) > k(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                hubo_cambio = True
        if not hubo_cambio:
            break
    return a


def seleccion(lista, clave=None):
    k = clave or _identidad
    a = list(lista)
    n = len(a)
    for i in range(n - 1):
        menor = i
        for j in range(i + 1, n):
            if k(a[j]) < k(a[menor]):
                menor = j
        a[i], a[menor] = a[menor], a[i]
    return a


def insercion(lista, clave=None):
    k = clave or _identidad
    a = list(lista)
    for i in range(1, len(a)):
        actual = a[i]
        j = i - 1
        while j >= 0 and k(a[j]) > k(actual):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual
    return a


def shell(lista, clave=None):
    k = clave or _identidad
    a = list(lista)
    salto = len(a) // 2
    while salto > 0:
        for i in range(salto, len(a)):
            actual = a[i]
            j = i
            while j >= salto and k(a[j - salto]) > k(actual):
                a[j] = a[j - salto]
                j -= salto
            a[j] = actual
        salto //= 2
    return a


def quicksort(lista, clave=None):
    k = clave or _identidad
    a = list(lista)

    def ordenar(bajo, alto):
        if bajo >= alto:
            return
        medio = (bajo + alto) // 2
        a[medio], a[alto] = a[alto], a[medio]        # pivote = elemento del medio
        pivote = k(a[alto])
        frontera = bajo
        for j in range(bajo, alto):
            if k(a[j]) < pivote:
                a[frontera], a[j] = a[j], a[frontera]
                frontera += 1
        a[frontera], a[alto] = a[alto], a[frontera]  # el pivote queda en su lugar definitivo
        ordenar(bajo, frontera - 1)
        ordenar(frontera + 1, alto)

    ordenar(0, len(a) - 1)
    return a


def mergesort(lista, clave=None):
    k = clave or _identidad
    a = list(lista)
    if len(a) <= 1:
        return a
    medio = len(a) // 2
    izq = mergesort(a[:medio], clave)
    der = mergesort(a[medio:], clave)
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if k(izq[i]) <= k(der[j]):                   # <= mantiene el orden de los iguales
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


ALGORITMOS = {
    "burbuja": burbuja,
    "selección": seleccion,
    "inserción": insercion,
    "shell": shell,
    "quicksort": quicksort,
    "mergesort": mergesort,
}
