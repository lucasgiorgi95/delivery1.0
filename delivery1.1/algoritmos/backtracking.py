"""Unidad 3: backtracking con una pila explícita.

Problema: elegir productos cuyo precio sume EXACTAMENTE el presupuesto del cliente.
Cada "estado" pendiente se guarda en la pila como (posición, suma, elegidos). Se prueba
primero tomar el producto; si el camino no sirve (la suma se pasó o se acabaron los
productos) se desapila y se vuelve al último punto de decisión: eso es retroceder."""
from estructuras.pila import PilaDinamica


def armar_combo(productos, presupuesto):
    """Devuelve una lista de productos que suma el presupuesto, o None si no hay forma.
    Cada producto se usa a lo sumo una vez. Peor caso exponencial: O(2^n)."""
    pila = PilaDinamica()
    pila.apilar((0, 0, ()))
    while not pila.esta_vacia():
        posicion, suma, elegidos = pila.desapilar()
        if suma == presupuesto and elegidos:
            return list(elegidos)
        if posicion == len(productos) or suma > presupuesto:
            continue                                   # camino sin salida: retrocede
        pila.apilar((posicion + 1, suma, elegidos))     # alternativa: no tomarlo (se prueba después)
        producto = productos[posicion]
        pila.apilar((posicion + 1, suma + producto.precio, elegidos + (producto,)))  # tomarlo
    return None
