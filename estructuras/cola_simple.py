"""
Cola Simple: implementada con nodos enlazados FIFO.
Puntero al frente y al final. Encolar y desencolar son O(1).
"""

from estructuras.nodo import Nodo


class ColaSimple:
    """Cola FIFO con nodos enlazados."""

    def __init__(self):
        self._frente = None
        self._final = None
        self._longitud = 0

    def esta_vacia(self):
        return self._frente is None

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self._frente = self._final = nuevo
        else:
            self._final.siguiente = nuevo
            self._final = nuevo
        self._longitud += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("Cola vacía")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._longitud -= 1
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            return None
        return self._frente.dato

    def longitud(self):
        return self._longitud

    def obtener_todos(self):
        """Devuelve lista Python con los datos en orden FIFO (sin modificar la cola)."""
        resultado = []
        actual = self._frente
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def __repr__(self):
        items = self.obtener_todos()
        return "ColaSimple([frente] " + " | ".join(str(x) for x in items) + " [final])"
