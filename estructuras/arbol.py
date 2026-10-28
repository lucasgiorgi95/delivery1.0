"""
Árboles binarios:
  - NodoArbol: nodo con código, producto, altura y punteros izq/der.
  - ABB: Árbol Binario de Búsqueda con insertar, buscar, eliminar,
         inorden, preorden y postorden.
  - AVL(ABB): extiende ABB con rotaciones y rebalanceo automático.
"""


# ─────────────────────────────────────────────
# Nodo del árbol
# ─────────────────────────────────────────────

class NodoArbol:
    def __init__(self, codigo, producto):
        self.codigo = codigo        # clave de búsqueda (int)
        self.producto = producto    # dato almacenado
        self.izq = None
        self.der = None
        self.altura = 1             # altura del subárbol rooted aquí


# ─────────────────────────────────────────────
# ABB — Árbol Binario de Búsqueda
# ─────────────────────────────────────────────

class ABB:
    """Árbol Binario de Búsqueda ordenado por código de producto."""

    def __init__(self):
        self.raiz = None

    # ── altura e inserción ──────────────────

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _insertar(self, nodo, codigo, producto):
        if nodo is None:
            return NodoArbol(codigo, producto)
        if codigo < nodo.codigo:
            nodo.izq = self._insertar(nodo.izq, codigo, producto)
        elif codigo > nodo.codigo:
            nodo.der = self._insertar(nodo.der, codigo, producto)
        else:
            nodo.producto = producto   # actualizar si ya existe
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        return nodo

    def insertar(self, codigo, producto):
        self.raiz = self._insertar(self.raiz, codigo, producto)

    # ── búsqueda ────────────────────────────

    def _buscar(self, nodo, codigo):
        if nodo is None:
            return None
        if codigo == nodo.codigo:
            return nodo.producto
        if codigo < nodo.codigo:
            return self._buscar(nodo.izq, codigo)
        return self._buscar(nodo.der, codigo)

    def buscar(self, codigo):
        """Devuelve el producto con ese código o None si no existe."""
        return self._buscar(self.raiz, codigo)

    # ── eliminación ─────────────────────────

    def _minimo(self, nodo):
        """Sucesor inorden: el nodo más pequeño del subárbol."""
        while nodo.izq:
            nodo = nodo.izq
        return nodo

    def _eliminar(self, nodo, codigo):
        if nodo is None:
            return None
        if codigo < nodo.codigo:
            nodo.izq = self._eliminar(nodo.izq, codigo)
        elif codigo > nodo.codigo:
            nodo.der = self._eliminar(nodo.der, codigo)
        else:
            # Encontrado: tres casos
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq
            # Dos hijos: reemplazar con sucesor inorden
            sucesor = self._minimo(nodo.der)
            nodo.codigo = sucesor.codigo
            nodo.producto = sucesor.producto
            nodo.der = self._eliminar(nodo.der, sucesor.codigo)
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        return nodo

    def eliminar(self, codigo):
        self.raiz = self._eliminar(self.raiz, codigo)

    # ── recorridos ──────────────────────────

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izq, resultado)
            resultado.append(nodo.producto)
            self._inorden(nodo.der, resultado)

    def inorden(self):
        """Devuelve lista de productos en orden ascendente de código."""
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.producto)
            self._preorden(nodo.izq, resultado)
            self._preorden(nodo.der, resultado)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, resultado):
        if nodo:
            self._postorden(nodo.izq, resultado)
            self._postorden(nodo.der, resultado)
            resultado.append(nodo.producto)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    # ── utilidad visual ─────────────────────

    def _arbol_str(self, nodo, prefijo="", es_izq=True):
        if nodo is None:
            return ""
        lineas = []
        if nodo.der:
            lineas.append(self._arbol_str(
                nodo.der,
                prefijo + ("│   " if es_izq else "    "),
                False
            ))
        lineas.append(prefijo + ("└── " if es_izq else "┌── ") + f"{nodo.codigo}")
        if nodo.izq:
            lineas.append(self._arbol_str(
                nodo.izq,
                prefijo + ("    " if es_izq else "│   "),
                True
            ))
        return "\n".join(lineas)

    def __repr__(self):
        if self.raiz is None:
            return "(árbol vacío)"
        return self._arbol_str(self.raiz)


# ─────────────────────────────────────────────
# AVL — Árbol AVL (extiende ABB con rotaciones)
# ─────────────────────────────────────────────

class AVL(ABB):
    """
    Árbol AVL: ABB que se autobalancea con rotaciones.
    Factor de balance = altura(izq) - altura(der).
    Se mantiene en [-1, 0, 1] después de cada operación.
    """

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.izq) - self._altura(nodo.der)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    # ── rotaciones ──────────────────────────

    def rotacion_der(self, y):
        """Rotación simple hacia la derecha sobre el nodo y."""
        #      y                x
        #     / \              / \
        #    x   T3    →    T1    y
        #   / \                  / \
        #  T1  T2              T2   T3
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def rotacion_izq(self, x):
        """Rotación simple hacia la izquierda sobre el nodo x."""
        #    x                  y
        #   / \                / \
        #  T1   y      →      x   T3
        #      / \           / \
        #     T2  T3        T1  T2
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def rotacion_der_izq(self, z):
        """Rotación doble: primero rotar hijo derecho a la derecha, luego z a la izquierda."""
        z.der = self.rotacion_der(z.der)
        return self.rotacion_izq(z)

    def rotacion_izq_der(self, z):
        """Rotación doble: primero rotar hijo izquierdo a la izquierda, luego z a la derecha."""
        z.izq = self.rotacion_izq(z.izq)
        return self.rotacion_der(z)

    # ── rebalancear ─────────────────────────

    def _rebalancear(self, nodo):
        """Aplica la rotación necesaria si el nodo está desbalanceado."""
        self._actualizar_altura(nodo)
        fb = self._factor_balance(nodo)

        # Caso Izquierda-Izquierda
        if fb > 1 and self._factor_balance(nodo.izq) >= 0:
            return self.rotacion_der(nodo)

        # Caso Izquierda-Derecha
        if fb > 1 and self._factor_balance(nodo.izq) < 0:
            return self.rotacion_izq_der(nodo)

        # Caso Derecha-Derecha
        if fb < -1 and self._factor_balance(nodo.der) <= 0:
            return self.rotacion_izq(nodo)

        # Caso Derecha-Izquierda
        if fb < -1 and self._factor_balance(nodo.der) > 0:
            return self.rotacion_der_izq(nodo)

        return nodo   # ya balanceado

    # ── insertar con rebalanceo ─────────────

    def _insertar(self, nodo, codigo, producto):
        # Inserción normal de ABB
        if nodo is None:
            return NodoArbol(codigo, producto)
        if codigo < nodo.codigo:
            nodo.izq = self._insertar(nodo.izq, codigo, producto)
        elif codigo > nodo.codigo:
            nodo.der = self._insertar(nodo.der, codigo, producto)
        else:
            nodo.producto = producto
            return nodo
        return self._rebalancear(nodo)

    # ── eliminar con rebalanceo ─────────────

    def _eliminar(self, nodo, codigo):
        if nodo is None:
            return None
        if codigo < nodo.codigo:
            nodo.izq = self._eliminar(nodo.izq, codigo)
        elif codigo > nodo.codigo:
            nodo.der = self._eliminar(nodo.der, codigo)
        else:
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq
            sucesor = self._minimo(nodo.der)
            nodo.codigo = sucesor.codigo
            nodo.producto = sucesor.producto
            nodo.der = self._eliminar(nodo.der, sucesor.codigo)
        return self._rebalancear(nodo)
