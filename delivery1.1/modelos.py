"""Datos del negocio: Producto y Pedido. Cada Pedido combina varias estructuras."""
from dataclasses import dataclass

from estructuras.listas import ListaDoble, ListaSimple
from estructuras.pila import PilaDinamica


@dataclass(frozen=True)
class Producto:
    codigo: int
    nombre: str
    precio: int


class Pedido:
    _proximo_id = 1

    def __init__(self, cliente, zona):
        self.id = Pedido._proximo_id
        Pedido._proximo_id += 1
        self.cliente = cliente
        self.zona = zona
        self.urgente = False
        self.repartidor = None
        self.items = ListaSimple()         # productos del pedido, en el orden cargado
        self._cargados = PilaDinamica()    # para "quitar el último" (deshacer)
        self.historial = ListaDoble()      # estados por los que pasó el pedido

    def agregar(self, producto):
        self.items.insertar_final(producto)
        self._cargados.apilar(producto)

    def quitar_ultimo(self):
        """Quita el último producto cargado. Lanza IndexError si no hay ninguno."""
        producto = self._cargados.desapilar()
        self.items.eliminar_ultimo()
        return producto

    def total(self):
        return sum(p.precio for p in self.items)

    def registrar(self, estado):
        self.historial.insertar_final(estado)
