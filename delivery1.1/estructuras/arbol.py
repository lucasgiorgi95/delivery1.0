"""Unidad 7: árboles binarios de búsqueda (ABB) y AVL.

En un ABB, para cada nodo: claves del subárbol izquierdo < clave < claves del derecho.
Buscar, insertar y eliminar cuestan O(altura): O(log n) si el árbol está equilibrado,
pero O(n) si se degenera en una "lista" (por ejemplo, insertando claves ya ordenadas).
El AVL se reequilibra con rotaciones y garantiza altura O(log n)."""


class NodoArbol:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1          # solo la usa el AVL


class ABB:
    def __init__(self):
        self.raiz = None
        self._cantidad = 0

    # --- operaciones del TAD ---
    def insertar(self, clave, valor=None):
        """Inserta; si la clave ya existe, reemplaza su valor."""
        self.raiz = self._insertar(self.raiz, clave, valor)

    def buscar(self, clave):
        """Devuelve el valor asociado a la clave, o None si no está."""
        actual = self.raiz
        while actual is not None:
            if clave == actual.clave:
                return actual.valor
            actual = actual.izq if clave < actual.clave else actual.der
        return None

    def eliminar(self, clave):
        """Elimina la clave. Lanza KeyError si no existe."""
        self.raiz = self._eliminar(self.raiz, clave)

    def altura(self):
        return self._altura(self.raiz)

    def __len__(self):
        return self._cantidad

    # --- recorridos (devuelven listas de (clave, valor)) ---
    def inorden(self):
        """Izquierdo, raíz, derecho: devuelve las claves ordenadas de menor a mayor."""
        resultado = []

        def visitar(n):
            if n is not None:
                visitar(n.izq)
                resultado.append((n.clave, n.valor))
                visitar(n.der)
        visitar(self.raiz)
        return resultado

    def preorden(self):
        """Raíz, izquierdo, derecho: sirve para copiar la forma del árbol."""
        resultado = []

        def visitar(n):
            if n is not None:
                resultado.append((n.clave, n.valor))
                visitar(n.izq)
                visitar(n.der)
        visitar(self.raiz)
        return resultado

    def postorden(self):
        """Izquierdo, derecho, raíz: los hijos se procesan antes que el padre."""
        resultado = []

        def visitar(n):
            if n is not None:
                visitar(n.izq)
                visitar(n.der)
                resultado.append((n.clave, n.valor))
        visitar(self.raiz)
        return resultado

    # --- internas ---
    def _insertar(self, nodo, clave, valor):
        if nodo is None:
            self._cantidad += 1
            return NodoArbol(clave, valor)
        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, clave, valor)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, clave, valor)
        else:
            nodo.valor = valor
            return nodo
        return self._equilibrar(nodo)

    def _eliminar(self, nodo, clave):
        if nodo is None:
            raise KeyError(clave)
        if clave < nodo.clave:
            nodo.izq = self._eliminar(nodo.izq, clave)
        elif clave > nodo.clave:
            nodo.der = self._eliminar(nodo.der, clave)
        else:
            if nodo.izq is None:             # caso 1 y 2: sin hijos o un solo hijo
                self._cantidad -= 1
                return nodo.der
            if nodo.der is None:
                self._cantidad -= 1
                return nodo.izq
            sucesor = nodo.der               # caso 3: dos hijos -> el menor del lado derecho
            while sucesor.izq is not None:
                sucesor = sucesor.izq
            nodo.clave, nodo.valor = sucesor.clave, sucesor.valor
            nodo.der = self._eliminar(nodo.der, sucesor.clave)
        return self._equilibrar(nodo)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    def _equilibrar(self, nodo):
        return nodo                           # el ABB común no reequilibra


class AVL(ABB):
    """ABB que mantiene |altura(izq) - altura(der)| <= 1 en todos sus nodos."""

    def __init__(self):
        super().__init__()
        self.rotaciones = 0

    def _alt(self, nodo):
        return nodo.altura if nodo else 0

    def _actualizar(self, nodo):
        nodo.altura = 1 + max(self._alt(nodo.izq), self._alt(nodo.der))

    def _rotar_derecha(self, y):
        x = y.izq
        y.izq = x.der
        x.der = y
        self._actualizar(y)
        self._actualizar(x)
        self.rotaciones += 1
        return x

    def _rotar_izquierda(self, x):
        y = x.der
        x.der = y.izq
        y.izq = x
        self._actualizar(x)
        self._actualizar(y)
        self.rotaciones += 1
        return y

    def _equilibrar(self, nodo):
        self._actualizar(nodo)
        factor = self._alt(nodo.izq) - self._alt(nodo.der)
        if factor > 1:
            if self._alt(nodo.izq.izq) < self._alt(nodo.izq.der):    # caso izquierda-derecha
                nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)
        if factor < -1:
            if self._alt(nodo.der.der) < self._alt(nodo.der.izq):    # caso derecha-izquierda
                nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)
        return nodo
