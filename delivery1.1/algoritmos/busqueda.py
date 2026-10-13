"""Unidad 6: búsqueda. Devuelven la posición del elemento o -1 si no está."""


def _identidad(x):
    return x


def secuencial(lista, objetivo, clave=None):
    """Recorre de a uno. Sirve con la lista en cualquier orden. O(n)."""
    k = clave or _identidad
    for i, elemento in enumerate(lista):
        if k(elemento) == objetivo:
            return i
    return -1


def binaria(lista, objetivo, clave=None):
    """Exige la lista ORDENADA por la misma clave. Descarta la mitad en cada paso: O(log n)."""
    k = clave or _identidad
    bajo, alto = 0, len(lista) - 1
    while bajo <= alto:
        medio = (bajo + alto) // 2
        valor = k(lista[medio])
        if valor == objetivo:
            return medio
        if valor < objetivo:
            bajo = medio + 1
        else:
            alto = medio - 1
    return -1


def binaria_recursiva(lista, objetivo, clave=None, bajo=0, alto=None):
    k = clave or _identidad
    if alto is None:
        alto = len(lista) - 1
    if bajo > alto:
        return -1
    medio = (bajo + alto) // 2
    valor = k(lista[medio])
    if valor == objetivo:
        return medio
    if valor < objetivo:
        return binaria_recursiva(lista, objetivo, clave, medio + 1, alto)
    return binaria_recursiva(lista, objetivo, clave, bajo, medio - 1)
