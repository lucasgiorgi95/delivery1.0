"""
Lista Doble: cada nodo apunta al siguiente y al anterior.
Permite recorrer en ambas direcciones e insertar/eliminar en extremos en O(1).
"""

from estructuras.nodo import NodoDoble


class ListaDoble:
    """Lista doblemente enlazada: cada nodo apunta al siguiente y al anterior."""

    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None

    def insertar_inicio(self, dato):
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self.cabeza = self.cola = nuevo
            return
        nuevo.siguiente = self.cabeza
        self.cabeza.anterior = nuevo
        self.cabeza = nuevo

    def insertar_final(self, dato):
        nuevo = NodoDoble(dato)
        if self.esta_vacia():
            self.cabeza = self.cola = nuevo
            return
        nuevo.anterior = self.cola
        self.cola.siguiente = nuevo
        self.cola = nuevo

    def eliminar(self, dato):
        """Elimina el primer nodo con ese dato exacto."""
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        """Devuelve lista Python con los datos de cabeza a cola."""
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def recorrer_inverso(self):
        """Devuelve lista Python con los datos de cola a cabeza."""
        resultado = []
        actual = self.cola
        while actual:
            resultado.append(actual.dato)
            actual = actual.anterior
        return resultado

    def longitud(self):
        cuenta = 0
        actual = self.cabeza
        while actual:
            cuenta += 1
            actual = actual.siguiente
        return cuenta

    def __repr__(self):
        items = self.recorrer()
        return " <-> ".join(str(x) for x in items)
