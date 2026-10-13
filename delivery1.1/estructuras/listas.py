"""Unidad 4: listas enlazadas simple, doble y circular."""
from estructuras.nodo import Nodo, NodoDoble


class ListaSimple:
    """Cada nodo apunta solo al siguiente. Se guarda solo la cabeza, así que
    insertar al final es O(n) (hay que recorrer) e insertar al inicio es O(1)."""

    def __init__(self):
        self._cabeza = None
        self._cantidad = 0

    def insertar_inicio(self, dato):
        self._cabeza = Nodo(dato, self._cabeza)
        self._cantidad += 1

    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo
        else:
            actual = self._cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._cantidad += 1

    def eliminar_ultimo(self):
        if self._cabeza is None:
            raise IndexError("La lista está vacía")
        if self._cabeza.siguiente is None:
            dato = self._cabeza.dato
            self._cabeza = None
        else:
            anterior = self._cabeza
            while anterior.siguiente.siguiente is not None:
                anterior = anterior.siguiente
            dato = anterior.siguiente.dato
            anterior.siguiente = None
        self._cantidad -= 1
        return dato

    def eliminar(self, condicion):
        """Elimina el primer elemento que cumple la condición. Devuelve True si eliminó."""
        anterior, actual = None, self._cabeza
        while actual is not None:
            if condicion(actual.dato):
                if anterior is None:
                    self._cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self._cantidad -= 1
                return True
            anterior, actual = actual, actual.siguiente
        return False

    def buscar(self, condicion):
        for dato in self:
            if condicion(dato):
                return dato
        return None

    def esta_vacia(self):
        return self._cabeza is None

    def __len__(self):
        return self._cantidad

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


class ListaDoble:
    """Cada nodo apunta al anterior y al siguiente; se guardan cabeza y cola.
    Se puede recorrer en ambos sentidos y insertar en cualquiera de los dos extremos en O(1)."""

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._cantidad = 0

    def insertar_inicio(self, dato):
        nuevo = NodoDoble(dato, None, self._cabeza)
        if self._cabeza is None:
            self._cola = nuevo
        else:
            self._cabeza.anterior = nuevo
        self._cabeza = nuevo
        self._cantidad += 1

    def insertar_final(self, dato):
        nuevo = NodoDoble(dato, self._cola, None)
        if self._cola is None:
            self._cabeza = nuevo
        else:
            self._cola.siguiente = nuevo
        self._cola = nuevo
        self._cantidad += 1

    def eliminar_ultimo(self):
        if self._cola is None:
            raise IndexError("La lista está vacía")
        dato = self._cola.dato
        self._cola = self._cola.anterior
        if self._cola is None:
            self._cabeza = None
        else:
            self._cola.siguiente = None
        self._cantidad -= 1
        return dato

    def esta_vacia(self):
        return self._cabeza is None

    def __len__(self):
        return self._cantidad

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def iter_inverso(self):
        actual = self._cola
        while actual is not None:
            yield actual.dato
            actual = actual.anterior


class ListaCircular:
    """El último nodo apunta de nuevo al primero. Se guarda solo una referencia al último:
    el primero es ultimo.siguiente. Sirve para turnos rotativos (round robin)."""

    def __init__(self):
        self._ultimo = None
        self._cantidad = 0

    def insertar(self, dato):
        """Agrega al final del círculo, en O(1)."""
        nuevo = Nodo(dato)
        if self._ultimo is None:
            nuevo.siguiente = nuevo
        else:
            nuevo.siguiente = self._ultimo.siguiente
            self._ultimo.siguiente = nuevo
        self._ultimo = nuevo
        self._cantidad += 1

    def siguiente_turno(self):
        """Devuelve el dato que está primero y lo pasa al final: da la vuelta sin fin."""
        if self._ultimo is None:
            raise IndexError("La lista está vacía")
        primero = self._ultimo.siguiente
        self._ultimo = primero
        return primero.dato

    def esta_vacia(self):
        return self._ultimo is None

    def __len__(self):
        return self._cantidad

    def __iter__(self):
        """Una sola vuelta, empezando por el primero."""
        if self._ultimo is None:
            return
        actual = self._ultimo.siguiente
        for _ in range(self._cantidad):
            yield actual.dato
            actual = actual.siguiente
