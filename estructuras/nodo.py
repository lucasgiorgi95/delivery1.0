"""
Módulo de nodos base para las estructuras de datos enlazadas.
Implementa Nodo simple y NodoDoble (con puntero anterior).
"""


class Nodo:
    """Nodo simple: guarda un dato y apunta al siguiente nodo."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

    def __repr__(self):
        return f"Nodo({self.dato!r})"


class NodoDoble:
    """Nodo doble: guarda un dato y apunta al siguiente y al anterior."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

    def __repr__(self):
        return f"NodoDoble({self.dato!r})"
