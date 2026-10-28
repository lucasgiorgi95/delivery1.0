"""
Modelos del dominio:
  - Producto: ítem del catálogo.
  - ItemPedido: producto + cantidad dentro de un pedido.
  - Combo: agrupación de ítems con descuento.
  - Pedido: pedido completo con lista de ítems, combos, pila para deshacer,
            historial de estados y metadatos.
"""

from estructuras.lista_simple  import ListaSimple
from estructuras.lista_doble   import ListaDoble
from estructuras.pila_dinamica import PilaDinamica


# ─────────────────────────────────────────────
# Producto
# ─────────────────────────────────────────────

class Producto:
    def __init__(self, codigo, nombre, precio, categoria):
        self.codigo = codigo          # int — clave del AVL
        self.nombre = nombre          # str
        self.precio = precio          # float
        self.categoria = categoria    # "comida" | "bebida"

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - ${self.precio:.2f}"

    def __repr__(self):
        return f"Producto({self.codigo}, {self.nombre!r}, {self.precio}, {self.categoria!r})"


# ─────────────────────────────────────────────
# Item Pedido
# ─────────────────────────────────────────────

class ItemPedido:
    def __init__(self, producto, cantidad=1):
        self.producto = producto      # Producto
        self.cantidad = int(cantidad)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return (f"{self.producto.nombre} x{self.cantidad} "
                f"= ${self.subtotal():.2f}")

    def __repr__(self):
        return f"ItemPedido({self.producto.codigo}, x{self.cantidad})"


# ─────────────────────────────────────────────
# Combo
# ─────────────────────────────────────────────

class Combo:
    def __init__(self, nombre, items, descuento=0.10):
        self.nombre = nombre          # str
        self.items = items            # list[ItemPedido]
        self.descuento = descuento    # float en [0, 1]

    def subtotal_sin_descuento(self):
        return sum(i.subtotal() for i in self.items)

    def total(self):
        return self.subtotal_sin_descuento() * (1 - self.descuento)

    def __str__(self):
        desc_pct = int(self.descuento * 100)
        return (f"Combo '{self.nombre}' ({desc_pct}% dto) "
                f"→ ${self.total():.2f}")

    def __repr__(self):
        return f"Combo({self.nombre!r}, items={len(self.items)}, dto={self.descuento})"


# ─────────────────────────────────────────────
# Pedido
# ─────────────────────────────────────────────

class Pedido:
    _contador = 0

    def __init__(self, cliente, tipo_entrega):
        Pedido._contador += 1
        self.numero = Pedido._contador
        self.cliente = cliente                    # str
        self.tipo_entrega = tipo_entrega          # "retira" | "delivery"
        self.items = ListaSimple()                # nodos de ItemPedido
        self.combos = []                          # list[Combo]
        self._cargados = PilaDinamica()           # pila para deshacer
        self.historial = ListaDoble()             # estados del pedido
        self.estado = "creado"
        self.urgente = False
        self.zona_destino = None
        self.historial.insertar_final("creado")

    # ── gestión de ítems ───────────────────

    def agregar_item(self, item):
        """Agrega un ItemPedido a la lista y lo apila para poder deshacer."""
        self.items.insertar_final(item)
        self._cargados.apilar(item)

    def agregar_combo(self, combo):
        self.combos.append(combo)
        self.historial.insertar_final(f"combo '{combo.nombre}' agregado")

    def quitar_ultimo(self):
        """Deshace el último ítem agregado (LIFO con pila)."""
        if not self._cargados.esta_vacia():
            item = self._cargados.desapilar()
            self.items.eliminar_por_condicion(lambda x: x is item)
            return item
        return None

    # ── estado ─────────────────────────────

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.historial.insertar_final(nuevo_estado)

    # ── total ──────────────────────────────

    def total(self):
        total = 0
        nodo = self.items.cabeza
        while nodo:
            total += nodo.dato.subtotal()
            nodo = nodo.siguiente
        for combo in self.combos:
            total += combo.total()
        return total

    # ── representación ─────────────────────

    def __str__(self):
        urgencia = "URGENTE" if self.urgente else "normal"
        return f"Pedido #{self.numero} - {self.cliente} ({urgencia})"

    def __repr__(self):
        return (f"Pedido(#{self.numero}, cliente={self.cliente!r}, "
                f"estado={self.estado!r}, urgente={self.urgente})")
