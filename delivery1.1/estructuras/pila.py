"""Unidad 3: pilas (LIFO). TAD Pila: apilar, desapilar, ver_tope, esta_vacia.

Dos implementaciones del mismo TAD: con arreglo de tamaño fijo (estática) y con nodos
enlazados (dinámica). Mismas operaciones, distinta representación."""
from estructuras.nodo import Nodo


class PilaEstatica:
    """Capacidad fija. Todas las operaciones son O(1)."""

    def __init__(self, capacidad):
        self._datos = [None] * capacidad
        self._tope = -1

    def apilar(self, dato):
        if self.esta_llena():
            raise OverflowError("La pila está llena")
        self._tope += 1
        self._datos[self._tope] = dato

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        dato = self._datos[self._tope]
        self._datos[self._tope] = None
        self._tope -= 1
        return dato

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self._datos[self._tope]

    def esta_vacia(self):
        return self._tope == -1

    def esta_llena(self):
        return self._tope == len(self._datos) - 1

    def __len__(self):
        return self._tope + 1


class PilaDinamica:
    """Sin límite de tamaño. El tope es el primer nodo; apilar y desapilar son O(1)."""

    def __init__(self):
        self._tope = None
        self._cantidad = 0

    def apilar(self, dato):
        self._tope = Nodo(dato, self._tope)
        self._cantidad += 1

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        self._cantidad -= 1
        return dato

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self._tope.dato

    def esta_vacia(self):
        return self._tope is None

    def __len__(self):
        return self._cantidad
