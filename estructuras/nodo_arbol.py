"""
NodoArbol: nodo base para los árboles binarios ABB y AVL.
Guarda código (clave), producto (dato), altura y punteros izq/der.
"""


class NodoArbol:
    """Nodo de árbol binario con clave (codigo) y dato (producto)."""

    def __init__(self, codigo, producto):
        self.codigo = codigo      # clave de búsqueda (int)
        self.producto = producto  # dato almacenado
        self.izq = None
        self.der = None
        self.altura = 1           # altura del subárbol con raíz aquí

    def __repr__(self):
        return f"NodoArbol({self.codigo})"
