"""
Pila Dinámica: implementada con nodos enlazados, sin límite de tamaño.
Las operaciones apilar, desapilar y ver_tope son O(1).
"""

from estructuras.nodo import Nodo


class PilaDinamica:
    """Pila LIFO con nodos enlazados (sin límite de tamaño)."""

    def __init__(self):
        self._tope = None   # nodo en el tope

    def esta_vacia(self):
        return self._tope is None

    def apilar(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self._tope
        self._tope = nuevo

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Pila dinámica vacía")
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        return dato

    def ver_tope(self):
        if self.esta_vacia():
            return None
        return self._tope.dato

    def longitud(self):
        cuenta = 0
        actual = self._tope
        while actual:
            cuenta += 1
            actual = actual.siguiente
        return cuenta

    def __repr__(self):
        items = []
        actual = self._tope
        while actual:
            items.append(str(actual.dato))
            actual = actual.siguiente
        return f"PilaDinamica(tope → [{', '.join(items)}])"
