# Compatibilidad: re-exporta desde los archivos individuales.
# Podés importar directamente desde nodo_arbol, abb o avl.
from estructuras.nodo_arbol import NodoArbol
from estructuras.abb        import ABB
from estructuras.avl        import AVL

__all__ = ["NodoArbol", "ABB", "AVL"]
