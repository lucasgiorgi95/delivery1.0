"""Unidad 3: colas (FIFO). TAD Cola: encolar, desencolar, ver_frente, esta_vacia."""
from estructuras.nodo import Nodo


class ColaSimple:
    """Cola dinámica con punteros al frente y al final: encolar y desencolar son O(1)."""

    def __init__(self):
        self._frente = None
        self._final = None
        self._cantidad = 0

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self._final is None:
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._cantidad += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._cantidad -= 1
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._frente.dato

    def esta_vacia(self):
        return self._frente is None

    def __len__(self):
        return self._cantidad

    def __iter__(self):
        actual = self._frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


class ColaCircular:
    """Cola de capacidad fija sobre un arreglo. Los índices dan la vuelta con el módulo (%),
    así los lugares liberados al desencolar se vuelven a usar."""

    def __init__(self, capacidad):
        self._datos = [None] * capacidad
        self._frente = 0
        self._cantidad = 0

    def encolar(self, dato):
        if self.esta_llena():
            raise OverflowError("La cola está llena")
        posicion = (self._frente + self._cantidad) % len(self._datos)
        self._datos[posicion] = dato
        self._cantidad += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        dato = self._datos[self._frente]
        self._datos[self._frente] = None
        self._frente = (self._frente + 1) % len(self._datos)
        self._cantidad -= 1
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._datos[self._frente]

    def esta_vacia(self):
        return self._cantidad == 0

    def esta_llena(self):
        return self._cantidad == len(self._datos)

    def __len__(self):
        return self._cantidad

    def __iter__(self):
        for i in range(self._cantidad):
            yield self._datos[(self._frente + i) % len(self._datos)]
