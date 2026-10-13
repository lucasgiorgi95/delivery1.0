"""Unidad 2: estructuras autorreferenciadas. Un nodo guarda un dato y una referencia
(puntero) a otro nodo del mismo tipo."""


class Nodo:
    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class NodoDoble:
    def __init__(self, dato, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente
