"""
Implementación de colas:
  - ColaSimple: nodos enlazados FIFO con puntero al frente y al final.
  - ColaCircular: arreglo fijo con índices que dan la vuelta con módulo.
"""

from estructuras.nodo import Nodo


# ─────────────────────────────────────────────
# Cola Simple
# ─────────────────────────────────────────────

class ColaSimple:
    """Cola FIFO con nodos enlazados. Encolar y desencolar son O(1)."""

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


# ─────────────────────────────────────────────
# Cola Circular
# ─────────────────────────────────────────────

class ColaCircular:
    """
    Cola FIFO con arreglo de tamaño fijo.
    Los índices se mueven con módulo (%) para reutilizar posiciones.
    """

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
            # Al estar llena, sobreescribimos el más antiguo (avanzamos el frente)
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
