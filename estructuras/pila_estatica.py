"""
Pila Estática: implementada con arreglo de tamaño fijo.
Las operaciones apilar, desapilar y ver_tope son O(1).
"""


class PilaEstatica:
    """Pila LIFO con arreglo de capacidad fija."""

    def __init__(self, capacidad=10):
        self.capacidad = capacidad
        self._datos = [None] * capacidad
        self._tope = -1   # índice del tope (-1 = vacía)

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
