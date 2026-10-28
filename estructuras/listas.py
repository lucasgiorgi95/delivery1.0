"""
Implementación de listas enlazadas:
  - ListaSimple: nodos con puntero solo al siguiente.
  - ListaDoble: nodos con puntero al siguiente y al anterior.
  - ListaCircular: el último nodo apunta al primero (turnos rotativos).
"""

from estructuras.nodo import Nodo, NodoDoble


# ─────────────────────────────────────────────
# Lista Simple
# ─────────────────────────────────────────────

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
        # Caso cabeza
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


# ─────────────────────────────────────────────
# Lista Doble
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# Lista Circular
# ─────────────────────────────────────────────

class ListaCircular:
    """
    Lista circular con nodos simples.
    El último nodo apunta de vuelta al primero.
    Se guarda referencia al último para poder insertar al final en O(1)
    y acceder al primero como ultimo.siguiente.
    """

    def __init__(self):
        self.ultimo = None   # el último nodo; ultimo.siguiente == primero

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
        """Avanza el puntero 'ultimo' al siguiente (rota hacia adelante)."""
        if self.esta_vacia():
            return None
        self.ultimo = self.ultimo.siguiente
        return self.ultimo.dato   # devuelve el nuevo "último" (el recién activado)

    def actual(self):
        """Devuelve el dato del nodo actual (siguiente al último = primero del turno)."""
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
        while actual.siguiente is not self.ultimo.siguiente or actual is self.ultimo:
            siguiente = actual.siguiente
            if siguiente.dato == dato:
                actual.siguiente = siguiente.siguiente
                if siguiente is self.ultimo:
                    self.ultimo = actual
                return True
            if actual is self.ultimo:
                break
            actual = actual.siguiente
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
