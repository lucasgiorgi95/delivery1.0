"""El local: junta todas las estructuras en un solo problema (sin print ni input).

Qué estructura resuelve qué:
  AVL                -> catálogo de productos, búsqueda por código en O(log n)
  Pila               -> "quitar el último" producto cargado en un pedido
  Lista simple       -> productos de un pedido
  Lista doble        -> historial de estados de un pedido (se recorre en ambos sentidos)
  Cola simple        -> pedidos normales, por orden de llegada
  Cola de prioridad  -> pedidos urgentes (heap): sale primero el que tiene menos minutos
  Cola circular      -> pizarra de "últimos pedidos listos" (capacidad fija)
  Lista circular     -> turnos rotativos de repartidores
  Grafo (lista ady.) -> mapa de zonas; BFS = ruta con menos paradas, DFS = zonas alcanzables
  Ordenamiento       -> catálogo por precio
  Búsqueda binaria   -> producto por precio exacto (sobre el catálogo ordenado por precio)
  Búsqueda secuencial-> producto por nombre
  Pila + postfija    -> calculadora de caja
  Pila + backtracking-> combo que suma justo el presupuesto
"""
from algoritmos import backtracking, busqueda, ordenamiento, postfija
from estructuras.arbol import AVL
from estructuras.cola import ColaCircular, ColaSimple
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.grafo import GrafoLista, bfs, camino_con_menos_paradas, dfs
from estructuras.listas import ListaCircular
from modelos import Pedido, Producto

CATALOGO_INICIAL = [
    Producto(104, "Gaseosa", 2000), Producto(101, "Hamburguesa simple", 5500),
    Producto(106, "Helado", 2500), Producto(103, "Papas fritas", 3000),
    Producto(107, "Cerveza", 3500), Producto(102, "Hamburguesa doble", 7500),
    Producto(105, "Pizza muzzarella", 8000),
]
REPARTIDORES = ["Rosa", "Tomás", "Lucía"]
CALLES = [("Local", "Centro"), ("Centro", "Norte"), ("Centro", "Sur"),
          ("Norte", "Costanera"), ("Sur", "Costanera")]
ZONA_RETIRO = "Retira en el local"


class ErrorDeNegocio(Exception):
    """Error pensado para mostrarse tal cual a quien usa el programa."""


class Local:
    def __init__(self):
        self.catalogo = AVL()
        for p in CATALOGO_INICIAL:
            self.catalogo.insertar(p.codigo, p)
        self.normales = ColaSimple()
        self.urgentes = ColaPrioridad()
        self.listos = ColaCircular(3)
        self.repartidores = ListaCircular()
        for nombre in REPARTIDORES:
            self.repartidores.insertar(nombre)
        self.zonas = GrafoLista()
        for a, b in CALLES:
            self.zonas.agregar_arista(a, b)
        self.zonas.agregar_vertice("Isla")           # sin calles: no se llega
        self.pedido_actual = None

    # --- armado de un pedido ---
    def iniciar_pedido(self, cliente, zona=""):
        if self.pedido_actual is not None:
            raise ErrorDeNegocio("Ya hay un pedido en armado. Confirmalo o cancelalo primero.")
        cliente = cliente.strip()
        if not cliente:
            raise ErrorDeNegocio("Escribí el nombre del cliente.")
        zona = zona.strip() or ZONA_RETIRO
        if zona != ZONA_RETIRO and zona not in self.zonas.vertices():
            raise ErrorDeNegocio(f"No conozco la zona «{zona}». Zonas: {', '.join(self.zonas.vertices())}.")
        self.pedido_actual = Pedido(cliente, zona)
        return self.pedido_actual

    def _pedido_abierto(self):
        if self.pedido_actual is None:
            raise ErrorDeNegocio("No hay un pedido en armado. Empezá uno nuevo.")
        return self.pedido_actual

    def agregar(self, codigo):
        pedido = self._pedido_abierto()
        producto = self.catalogo.buscar(codigo)
        if producto is None:
            raise ErrorDeNegocio(f"No existe el producto {codigo}.")
        pedido.agregar(producto)
        return producto

    def quitar_ultimo(self):
        pedido = self._pedido_abierto()
        try:
            return pedido.quitar_ultimo()
        except IndexError:
            raise ErrorDeNegocio("El pedido no tiene productos para quitar.")

    def cancelar(self):
        self._pedido_abierto()
        self.pedido_actual = None

    def confirmar(self, urgente=False, minutos=15):
        pedido = self._pedido_abierto()
        if pedido.items.esta_vacia():
            raise ErrorDeNegocio("Agregá al menos un producto antes de confirmar.")
        if pedido.zona != ZONA_RETIRO and self.ruta(pedido.zona) is None:
            raise ErrorDeNegocio(f"No hacemos envíos a {pedido.zona}.")
        pedido.urgente = urgente
        pedido.registrar("Confirmado")
        if urgente:
            self.urgentes.encolar(pedido, minutos)
        else:
            self.normales.encolar(pedido)
        self.pedido_actual = None
        return pedido

    # --- despacho ---
    def despachar(self):
        """Los urgentes salen primero; después los normales, por orden de llegada."""
        if not self.urgentes.esta_vacia():
            pedido = self.urgentes.desencolar()
        elif not self.normales.esta_vacia():
            pedido = self.normales.desencolar()
        else:
            raise ErrorDeNegocio("No hay pedidos en espera.")
        if pedido.zona != ZONA_RETIRO:
            pedido.repartidor = self.repartidores.siguiente_turno()
        pedido.registrar("Despachado")
        if self.listos.esta_llena():
            self.listos.desencolar()                  # la pizarra solo muestra los últimos 3
        self.listos.encolar(pedido)
        return pedido

    def en_espera(self):
        """Pedidos en el orden en que se despacharían."""
        return self.urgentes.en_orden_de_salida() + list(self.normales)

    # --- catálogo ---
    def productos_por_codigo(self):
        return [p for _, p in self.catalogo.inorden()]

    def productos_por_precio(self, algoritmo="mergesort"):
        funciones = {"mergesort": ordenamiento.mergesort, "quicksort": ordenamiento.quicksort}
        return funciones[algoritmo](self.productos_por_codigo(), clave=lambda p: p.precio)

    def buscar_por_precio(self, precio):
        """Búsqueda binaria sobre el catálogo ordenado por precio."""
        ordenados = self.productos_por_precio()
        posicion = busqueda.binaria(ordenados, precio, clave=lambda p: p.precio)
        return None if posicion == -1 else ordenados[posicion]

    def buscar_por_nombre(self, texto):
        """Búsqueda secuencial: no hay orden por nombre."""
        productos = self.productos_por_codigo()
        texto = texto.strip().lower()
        posicion = busqueda.secuencial(productos, texto, clave=lambda p: p.nombre.lower())
        return None if posicion == -1 else productos[posicion]

    # --- zonas ---
    def ruta(self, zona):
        return camino_con_menos_paradas(self.zonas, "Local", zona)

    def zonas_alcanzables(self):
        return [z for z in dfs(self.zonas, "Local") if z != "Local"]

    def recorrido_por_anchura(self):
        return bfs(self.zonas, "Local")

    # --- herramientas ---
    def combo(self, presupuesto):
        productos = self.productos_por_precio()
        return backtracking.armar_combo(productos, presupuesto)

    def calcular(self, cuenta):
        try:
            return postfija.calcular(cuenta)
        except ValueError as e:
            raise ErrorDeNegocio(str(e))
