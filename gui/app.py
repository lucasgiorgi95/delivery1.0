"""
Ventana principal del sistema de pedidos.
Crea las instancias globales compartidas y organiza las pestañas.
"""

import tkinter as tk
from tkinter import ttk

# ── Estructuras de datos ───────────────────────────────────────────────────
from estructuras.arbol        import AVL
from estructuras.cola         import ColaSimple, ColaCircular
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.grafo        import GrafoLista
from estructuras.listas       import ListaCircular

# ── Datos iniciales ────────────────────────────────────────────────────────
from datos.productos_iniciales import PRODUCTOS_INICIALES

# ── Paneles GUI ────────────────────────────────────────────────────────────
from gui.panel_pedidos      import PanelPedidos
from gui.panel_despacho     import PanelDespacho
from gui.panel_catalogo     import PanelCatalogo
from gui.panel_zonas        import PanelZonas
from gui.panel_estructuras  import PanelEstructuras
from gui.panel_repartidores import PanelRepartidores


def _crear_grafo_zonas():
    """Construye el grafo de zonas de delivery con las conexiones del enunciado."""
    g = GrafoLista()
    for zona in ["Local", "Norte", "Sur", "Costanera", "Isla"]:
        g.agregar_vertice(zona)
    g.agregar_arista("Local",     "Norte")
    g.agregar_arista("Local",     "Sur")
    g.agregar_arista("Norte",     "Costanera")
    g.agregar_arista("Sur",       "Costanera")
    g.agregar_arista("Costanera", "Isla")
    return g


def _crear_lista_repartidores():
    """Crea la lista circular con los repartidores iniciales."""
    lista = ListaCircular()
    for nombre in ["Ana", "Juan", "Pedro"]:
        lista.insertar(nombre)
    return lista


def _cargar_catalogo():
    """Inserta todos los productos iniciales en el AVL."""
    catalogo = AVL()
    for p in PRODUCTOS_INICIALES:
        catalogo.insertar(p.codigo, p)
    return catalogo


class App(tk.Tk):
    """Ventana principal con ttk.Notebook y estructuras compartidas."""

    def __init__(self):
        super().__init__()
        self.title("Sistema de Pedidos — Local de Comidas v2.0")
        self.geometry("960x680")
        self.minsize(820, 580)

        # Tema visual
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        self._aplicar_estilos(estilo)

        # ── Instancias globales compartidas ───────
        self.catalogo           = _cargar_catalogo()
        self.cola_pedidos       = ColaSimple()
        self.cola_urgentes      = ColaPrioridad()
        self.cola_recientes     = ColaCircular(3)
        self.grafo_zonas        = _crear_grafo_zonas()
        self.lista_repartidores = _crear_lista_repartidores()

        # ── Notebook ──────────────────────────────
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill="both", expand=True, padx=6, pady=6)

        self._agregar_pestanias()

        # Barra de estado
        self._barra_estado = ttk.Label(
            self, text="Sistema listo  —  Catálogo cargado con "
                       f"{len(self.catalogo.inorden())} productos.",
            relief="sunken", anchor="w", padding=(6, 2)
        )
        self._barra_estado.pack(fill="x", side="bottom")

    # ─────────────────────────────────────────────
    # Pestañas
    # ─────────────────────────────────────────────

    def _agregar_pestanias(self):
        nb = self._notebook

        panel_pedidos = PanelPedidos(
            nb,
            catalogo=self.catalogo,
            cola_pedidos=self.cola_pedidos,
            cola_urgentes=self.cola_urgentes,
        )
        nb.add(panel_pedidos, text="  📋 Nuevo Pedido  ")

        panel_despacho = PanelDespacho(
            nb,
            cola_pedidos=self.cola_pedidos,
            cola_urgentes=self.cola_urgentes,
            cola_recientes=self.cola_recientes,
            lista_repartidores=self.lista_repartidores,
        )
        nb.add(panel_despacho, text="  🚀 Despacho  ")

        panel_catalogo = PanelCatalogo(nb, catalogo=self.catalogo)
        nb.add(panel_catalogo, text="  📦 Catálogo  ")

        panel_zonas = PanelZonas(nb, grafo_zonas=self.grafo_zonas)
        nb.add(panel_zonas, text="  🗺 Zonas  ")

        panel_estructuras = PanelEstructuras(
            nb,
            catalogo=self.catalogo,
            cola_pedidos=self.cola_pedidos,
            cola_urgentes=self.cola_urgentes,
            cola_recientes=self.cola_recientes,
            lista_repartidores=self.lista_repartidores,
        )
        nb.add(panel_estructuras, text="  🔬 Estructuras  ")

        panel_repartidores = PanelRepartidores(
            nb, lista_repartidores=self.lista_repartidores
        )
        nb.add(panel_repartidores, text="  👥 Repartidores  ")

        # Refrescar Despacho al cambiar de pestaña
        nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

    # ─────────────────────────────────────────────
    # Eventos
    # ─────────────────────────────────────────────

    def _on_tab_change(self, _event):
        """Refresca el panel de despacho al activarlo."""
        widget = self._notebook.nametowidget(self._notebook.select())
        if isinstance(widget, PanelDespacho):
            widget.actualizar()

    # ─────────────────────────────────────────────
    # Estilos
    # ─────────────────────────────────────────────

    def _aplicar_estilos(self, estilo):
        BG        = "#f5f5f5"
        FG        = "#212121"
        ACCENT    = "#1565c0"
        BTN_BG    = "#1976d2"
        BTN_FG    = "white"
        TAB_SEL   = "#ffffff"
        TAB_BG    = "#e0e0e0"

        self.configure(bg=BG)
        estilo.configure(".",          background=BG, foreground=FG,
                         font=("Segoe UI", 9))
        estilo.configure("TFrame",     background=BG)
        estilo.configure("TLabelframe",       background=BG, relief="groove")
        estilo.configure("TLabelframe.Label", background=BG,
                         foreground=ACCENT, font=("Segoe UI", 9, "bold"))
        estilo.configure("TLabel",     background=BG, foreground=FG)
        estilo.configure("TButton",    background=BTN_BG, foreground=BTN_FG,
                         padding=(8, 4), font=("Segoe UI", 9))
        estilo.map("TButton",
                   background=[("active", "#1565c0"), ("pressed", "#0d47a1")])
        estilo.configure("TEntry",     fieldbackground="white", foreground=FG)
        estilo.configure("TCombobox",  fieldbackground="white", foreground=FG)
        estilo.configure("TNotebook",  background=TAB_BG)
        estilo.configure("TNotebook.Tab",
                         background=TAB_BG, foreground=FG,
                         padding=(10, 5), font=("Segoe UI", 9))
        estilo.map("TNotebook.Tab",
                   background=[("selected", TAB_SEL)],
                   foreground=[("selected", ACCENT)])
        estilo.configure("Treeview",
                         background="white", fieldbackground="white",
                         foreground=FG, rowheight=22)
        estilo.configure("Treeview.Heading",
                         background=TAB_BG, foreground=ACCENT,
                         font=("Segoe UI", 9, "bold"))
        estilo.map("Treeview",
                   background=[("selected", "#bbdefb")],
                   foreground=[("selected", FG)])
