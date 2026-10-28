"""
Implementación de pilas:
  - PilaEstatica: arreglo de tamaño fijo (lista Python de capacidad limitada).
  - PilaDinamica: nodos enlazados sin límite de tamaño.
"""

from estructuras.nodo import Nodo


# ─────────────────────────────────────────────
# Pila Estática
# ─────────────────────────────────────────────

class PilaEstatica:
    """Pila LIFO implementada con arreglo de tamaño fijo."""

    def __init__(self, capacidad=10):
        self.capacidad = capacidad
        self._datos = [None] * capacidad
        self._tope = -1   # índice del tope actual (-1 = vacía)

    def esta_vacia(self):
        return self._tope == -1

    def esta_llena(self):
        return self._tope == self.capacidad - 1

    def apilar(self, dato):
        if self.esta_llena():
            raise OverflowError("Pila estática llena")
        self._tope += 1
        self._datos[self._tope] = dato

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Pila estática vacía")
        dato = self._datos[self._tope]
        self._datos[self._tope] = None
        self._tope -= 1
        return dato

    def ver_tope(self):
        if self.esta_vacia():
            return None
        return self._datos[self._tope]

    def longitud(self):
        return self._tope + 1

    def __repr__(self):
        items = [str(self._datos[i]) for i in range(self._tope + 1)]
        return f"PilaEstatica(tope → [{', '.join(reversed(items))}])"


# ─────────────────────────────────────────────
# Pila Dinámica
# ─────────────────────────────────────────────

class PilaDinamica:
    """Pila LIFO implementada con nodos enlazados (sin límite de tamaño)."""

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
