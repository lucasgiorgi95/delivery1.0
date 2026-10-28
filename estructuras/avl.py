"""
AVL — Árbol AVL (extiende ABB con rotaciones automáticas).
Factor de balance = altura(izq) - altura(der).
Se mantiene en [-1, 0, 1] después de cada inserción/eliminación.
Garantiza O(log n) para buscar, insertar y eliminar siempre.
"""

from estructuras.abb import ABB
from estructuras.nodo_arbol import NodoArbol


class AVL(ABB):
    """
    Árbol AVL: ABB que se autobalancea con 4 tipos de rotaciones.
      - Rotación simple derecha       (caso Izquierda-Izquierda)
      - Rotación simple izquierda     (caso Derecha-Derecha)
      - Rotación doble izquierda-derecha (caso Izquierda-Derecha)
      - Rotación doble derecha-izquierda (caso Derecha-Izquierda)
    """

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.izq) - self._altura(nodo.der)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    # ── rotaciones simples ───────────────────

    def rotacion_der(self, y):
        """Rotación simple a la derecha sobre y.
              y              x
             / \\            / \\
            x   T3   →    T1   y
           / \\               / \\
          T1  T2            T2  T3
        """
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def rotacion_izq(self, x):
        """Rotación simple a la izquierda sobre x.
           x                y
          / \\              / \\
         T1   y    →      x   T3
             / \\         / \\
            T2  T3       T1  T2
        """
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    # ── rotaciones dobles ────────────────────

    def rotacion_izq_der(self, z):
        """Rotación doble: rotar hijo izquierdo a la izquierda, luego z a la derecha."""
        z.izq = self.rotacion_izq(z.izq)
        return self.rotacion_der(z)

    def rotacion_der_izq(self, z):
        """Rotación doble: rotar hijo derecho a la derecha, luego z a la izquierda."""
        z.der = self.rotacion_der(z.der)
        return self.rotacion_izq(z)

    # ── rebalancear ──────────────────────────

    def _rebalancear(self, nodo):
        """Detecta el caso de desbalanceo y aplica la rotación correcta."""
        self._actualizar_altura(nodo)
        fb = self._factor_balance(nodo)

        # Izquierda-Izquierda
        if fb > 1 and self._factor_balance(nodo.izq) >= 0:
            return self.rotacion_der(nodo)
        # Izquierda-Derecha
        if fb > 1 and self._factor_balance(nodo.izq) < 0:
            return self.rotacion_izq_der(nodo)
        # Derecha-Derecha
        if fb < -1 and self._factor_balance(nodo.der) <= 0:
            return self.rotacion_izq(nodo)
        # Derecha-Izquierda
        if fb < -1 and self._factor_balance(nodo.der) > 0:
            return self.rotacion_der_izq(nodo)

        return nodo   # ya balanceado

    # ── inserción con rebalanceo ─────────────

    def _insertar(self, nodo, codigo, producto):
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

    # ── eliminación con rebalanceo ───────────

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
