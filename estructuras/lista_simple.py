"""
Lista Simple: cada nodo apunta solo al siguiente (puntero único).
Insertar al inicio es O(1); insertar al final es O(n).
"""

from estructuras.nodo import Nodo


class ListaSimple:
    """Lista enlazada simple: cada nodo apunta solo al siguiente."""

    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def eliminar_por_condicion(self, condicion):
        """Elimina el primer nodo cuyo dato cumpla condicion(dato) == True."""
        if self.esta_vacia():
            return False
        if condicion(self.cabeza.dato):
            self.cabeza = self.cabeza.siguiente
            return True
        actual = self.cabeza
        while actual.siguiente:
            if condicion(actual.siguiente.dato):
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        """Devuelve lista Python con los datos en orden."""
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
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
        return " -> ".join(str(x) for x in items) + " -> None"
