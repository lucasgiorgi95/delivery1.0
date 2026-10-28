"""
Cola Circular: arreglo fijo donde los índices dan la vuelta con módulo (%).
Al encolar cuando está llena, el elemento más antiguo se sobreescribe.
"""


class ColaCircular:
    """Cola FIFO con arreglo de tamaño fijo e índices circulares."""

    def __init__(self, capacidad=5):
        self.capacidad = capacidad
        self._datos = [None] * capacidad
        self._frente = 0
        self._final = 0
        self._longitud = 0

    def esta_vacia(self):
        return self._longitud == 0

    def esta_llena(self):
        return self._longitud == self.capacidad

    def encolar(self, dato):
        if self.esta_llena():
            # Sobreescribe el más antiguo y avanza el frente
            self._datos[self._final % self.capacidad] = dato
            self._frente = (self._frente + 1) % self.capacidad
            self._final = (self._final + 1) % self.capacidad
        else:
            self._datos[self._final] = dato
            self._final = (self._final + 1) % self.capacidad
            self._longitud += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("Cola circular vacía")
        dato = self._datos[self._frente]
        self._datos[self._frente] = None
        self._frente = (self._frente + 1) % self.capacidad
        self._longitud -= 1
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            return None
        return self._datos[self._frente]

    def longitud(self):
        return self._longitud

    def obtener_todos(self):
        """Devuelve lista Python con los datos en orden FIFO."""
        resultado = []
        for i in range(self._longitud):
            idx = (self._frente + i) % self.capacidad
            resultado.append(self._datos[idx])
        return resultado

    def __repr__(self):
        items = self.obtener_todos()
        return (f"ColaCircular(cap={self.capacidad}) "
                "[" + ", ".join(str(x) for x in items) + "]")
