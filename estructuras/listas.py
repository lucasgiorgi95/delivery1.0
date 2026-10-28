# Compatibilidad: re-exporta desde los archivos individuales.
# Podés importar directamente desde lista_simple, lista_doble o lista_circular.
from estructuras.lista_simple   import ListaSimple
from estructuras.lista_doble    import ListaDoble
from estructuras.lista_circular import ListaCircular

__all__ = ["ListaSimple", "ListaDoble", "ListaCircular"]
