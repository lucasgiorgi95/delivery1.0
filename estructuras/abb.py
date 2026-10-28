"""
ABB — Árbol Binario de Búsqueda.
Para cada nodo: subárbol izquierdo tiene claves menores,
subárbol derecho tiene claves mayores.
Buscar, insertar y eliminar son O(log n) si está balanceado.
"""

from estructuras.nodo_arbol import NodoArbol


class ABB:
    """Árbol Binario de Búsqueda ordenado por código de producto."""

    def __init__(self):
        self.raiz = None

    # ── altura ──────────────────────────────

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    # ── inserción ───────────────────────────

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
            # Tres casos de eliminación
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
        """Lista de productos en orden ascendente de código."""
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

    # ── representación visual ────────────────

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
