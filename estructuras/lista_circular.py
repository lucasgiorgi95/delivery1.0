"""
Lista Circular: el último nodo apunta de vuelta al primero.
Ideal para turnos rotativos: nunca tiene fin.
Se guarda referencia al último nodo; el primero es ultimo.siguiente.
"""

from estructuras.nodo import Nodo


class ListaCircular:
    """
    Lista circular con nodos simples.
    El último nodo apunta de vuelta al primero.
    Se guarda referencia al último para insertar al final en O(1)
    y acceder al primero como ultimo.siguiente.
    """

    def __init__(self):
        self.ultimo = None   # ultimo.siguiente == primero

    def esta_vacia(self):
        return self.ultimo is None

    def insertar(self, dato):
        """Inserta al final del ciclo."""
        nuevo = Nodo(dato)
        if self.esta_vacia():
            nuevo.siguiente = nuevo   # apunta a sí mismo
            self.ultimo = nuevo
        else:
            nuevo.siguiente = self.ultimo.siguiente   # nuevo apunta al primero
            self.ultimo.siguiente = nuevo              # anterior último apunta al nuevo
            self.ultimo = nuevo                        # nuevo es el último

    def siguiente_turno(self):
        """Avanza el puntero 'ultimo' (rota hacia adelante). Devuelve el nuevo actual."""
        if self.esta_vacia():
            return None
        self.ultimo = self.ultimo.siguiente
        return self.ultimo.dato

    def actual(self):
        """Devuelve el dato del primer nodo del turno (siguiente al último)."""
        if self.esta_vacia():
            return None
        return self.ultimo.siguiente.dato

    def eliminar(self, dato):
        """Elimina el primer nodo con ese dato."""
        if self.esta_vacia():
            return False
        primero = self.ultimo.siguiente
        # caso un solo nodo
        if primero is self.ultimo and primero.dato == dato:
            self.ultimo = None
            return True
        actual = self.ultimo
        while True:
            siguiente = actual.siguiente
            if siguiente.dato == dato:
                actual.siguiente = siguiente.siguiente
                if siguiente is self.ultimo:
                    self.ultimo = actual
                return True
            actual = actual.siguiente
            if actual is self.ultimo:
                break
        return False

    def recorrer(self):
        """Devuelve lista Python con todos los datos del ciclo."""
        if self.esta_vacia():
            return []
        resultado = []
        inicio = self.ultimo.siguiente
        actual = inicio
        while True:
            resultado.append(actual.dato)
            actual = actual.siguiente
            if actual is inicio:
                break
        return resultado

    def longitud(self):
        if self.esta_vacia():
            return 0
        cuenta = 1
        inicio = self.ultimo.siguiente
        actual = inicio.siguiente
        while actual is not inicio:
            cuenta += 1
            actual = actual.siguiente
        return cuenta

    def __repr__(self):
        items = self.recorrer()
        if not items:
            return "(vacía)"
        return " -> ".join(str(x) for x in items) + " -> (inicio)"
