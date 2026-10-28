"""
Panel Estructuras — panel educativo para visualizar las estructuras de datos.
"""

import tkinter as tk
from tkinter import ttk


DESCRIPCIONES = {
    "Lista Simple": (
        "Lista Simple (ListaSimple)\n"
        "══════════════════════════\n"
        "Cada nodo apunta solo al siguiente.\n"
        "• insertar_inicio: O(1)\n"
        "• insertar_final:  O(n)  (recorre hasta el último)\n"
        "• eliminar por condición: O(n)\n\n"
        "Uso en el proyecto: guarda los ítems de cada Pedido."
    ),
    "Lista Doble": (
        "Lista Doble (ListaDoble)\n"
        "════════════════════════\n"
        "Cada nodo apunta al siguiente Y al anterior.\n"
        "• insertar en cualquier extremo: O(1)\n"
        "• recorrer hacia atrás: O(n)\n\n"
        "Uso en el proyecto: historial de estados del Pedido."
    ),
    "Lista Circular": (
        "Lista Circular (ListaCircular)\n"
        "══════════════════════════════\n"
        "El último nodo apunta de vuelta al primero.\n"
        "• siguiente_turno(): O(1)\n"
        "• nunca tiene fin → ideal para turnos.\n\n"
        "Uso en el proyecto: turnos rotativos de repartidores."
    ),
    "Pila Estática": (
        "Pila Estática (PilaEstatica)\n"
        "════════════════════════════\n"
        "Arreglo de tamaño fijo. LIFO.\n"
        "• apilar / desapilar: O(1)\n"
        "• capacidad máxima fija.\n\n"
        "Uso en el proyecto: demostración / educativo."
    ),
    "Pila Dinámica": (
        "Pila Dinámica (PilaDinamica)\n"
        "════════════════════════════\n"
        "Nodos enlazados. LIFO. Sin límite de tamaño.\n"
        "• apilar / desapilar: O(1)\n\n"
        "Uso en el proyecto: botón 'Quitar último' del pedido.\n"
        "También usada internamente en DFS del grafo."
    ),
    "Cola Simple": (
        "Cola Simple (ColaSimple)\n"
        "════════════════════════\n"
        "Nodos enlazados. FIFO.\n"
        "• encolar / desencolar: O(1)\n\n"
        "Uso en el proyecto: cola de pedidos normales en espera."
    ),
    "Cola Circular": (
        "Cola Circular (ColaCircular)\n"
        "════════════════════════════\n"
        "Arreglo fijo con índices módulo (%).\n"
        "• encolar / desencolar: O(1)\n"
        "• sobreescribe el más viejo al llenarse.\n\n"
        "Uso en el proyecto: pizarra de últimos 3 despachados."
    ),
    "Cola Prioridad": (
        "Cola de Prioridad (ColaPrioridad)\n"
        "══════════════════════════════════\n"
        "Heap binario mínimo en arreglo.\n"
        "• encolar / desencolar: O(log n)\n"
        "• prioridad=0 → urgente, prioridad=1 → normal\n"
        "• desempate por orden de llegada.\n\n"
        "Uso en el proyecto: cola de pedidos urgentes."
    ),
    "ABB": (
        "Árbol Binario de Búsqueda (ABB)\n"
        "═══════════════════════════════\n"
        "Izquierda < raíz < derecha.\n"
        "• buscar / insertar / eliminar: O(log n) si balanceado\n"
        "  pero O(n) si se insertan claves en orden.\n"
        "• inorden devuelve claves ordenadas.\n\n"
        "Uso en el proyecto: base del AVL del catálogo."
    ),
    "AVL": (
        "Árbol AVL (AVL)\n"
        "═══════════════\n"
        "ABB autobalanceado con rotaciones.\n"
        "• factor de balance ∈ {-1, 0, 1} siempre.\n"
        "• buscar / insertar / eliminar: O(log n) GARANTIZADO.\n"
        "• 4 tipos de rotación: der, izq, der-izq, izq-der.\n\n"
        "Uso en el proyecto: catálogo de productos."
    ),
    "Grafo": (
        "Grafo (GrafoLista)\n"
        "══════════════════\n"
        "Lista de adyacencia: O(V+A) memoria.\n"
        "• BFS con ColaSimple → ruta más corta.\n"
        "• DFS con PilaDinamica → zonas alcanzables.\n\n"
        "Uso en el proyecto: mapa de zonas de delivery."
    ),
}


class PanelEstructuras(ttk.Frame):
    """Pestaña 'Estructuras': visualiza internamente cada estructura."""

    def __init__(self, parent, catalogo, cola_pedidos,
                 cola_urgentes, cola_recientes,
                 lista_repartidores, **kwargs):
        super().__init__(parent, **kwargs)
        self.catalogo           = catalogo
        self.cola_pedidos       = cola_pedidos
        self.cola_urgentes      = cola_urgentes
        self.cola_recientes     = cola_recientes
        self.lista_repartidores = lista_repartidores
        self._construir_ui()

    # ─────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────

    def _construir_ui(self):
        self.configure(padding=10)

        ttk.Label(self, text="Visualizador de Estructuras de Datos",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

        frm_ctrl = ttk.Frame(self)
        frm_ctrl.pack(fill="x", pady=(0, 6))

        ttk.Label(frm_ctrl, text="Estructura:").pack(side="left", padx=(0, 6))
        self._var_est = tk.StringVar(value="AVL")
        opciones = list(DESCRIPCIONES.keys())
        self._cb_est = ttk.Combobox(frm_ctrl, textvariable=self._var_est,
                                    values=opciones, state="readonly", width=20)
        self._cb_est.pack(side="left", padx=(0, 10))
        self._cb_est.bind("<<ComboboxSelected>>", lambda _: self._mostrar())

        ttk.Button(frm_ctrl, text="Ver estructura",
                   command=self._mostrar).pack(side="left", padx=(0, 4))

        # Botones de recorrido de árbol
        self._frm_arbol = ttk.Frame(frm_ctrl)
        self._frm_arbol.pack(side="left", padx=(10, 0))
        ttk.Button(self._frm_arbol, text="Inorden",
                   command=lambda: self._mostrar_recorrido("inorden")).pack(side="left", padx=2)
        ttk.Button(self._frm_arbol, text="Preorden",
                   command=lambda: self._mostrar_recorrido("preorden")).pack(side="left", padx=2)
        ttk.Button(self._frm_arbol, text="Postorden",
                   command=lambda: self._mostrar_recorrido("postorden")).pack(side="left", padx=2)

        # Descripción de la estructura
        frm_desc = ttk.LabelFrame(self, text="Descripción", padding=8)
        frm_desc.pack(fill="x", pady=(0, 6))
        self._lbl_desc = ttk.Label(frm_desc, text="", justify="left",
                                   font=("Segoe UI", 9), wraplength=700)
        self._lbl_desc.pack(anchor="w")

        # Text de contenido
        frm_txt = ttk.LabelFrame(self, text="Contenido actual de la estructura", padding=8)
        frm_txt.pack(fill="both", expand=True)

        self._txt = tk.Text(frm_txt, font=("Courier New", 9),
                            state="disabled", background="#f5f5f5")
        sc = ttk.Scrollbar(frm_txt, orient="vertical", command=self._txt.yview)
        self._txt.configure(yscrollcommand=sc.set)
        self._txt.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        self._mostrar()

    # ─────────────────────────────────────────────
    # Lógica
    # ─────────────────────────────────────────────

    def _escribir(self, texto):
        self._txt.config(state="normal")
        self._txt.delete("1.0", "end")
        self._txt.insert("end", texto)
        self._txt.config(state="disabled")

    def _mostrar(self):
        est = self._var_est.get()
        desc = DESCRIPCIONES.get(est, "")
        self._lbl_desc.config(text=desc)

        if est == "Lista Simple":
            self._escribir("(la ListaSimple de ítems existe dentro de cada Pedido;\n"
                           "no hay una instancia global para mostrar aquí)")
        elif est == "Lista Doble":
            self._escribir("(la ListaDoble de historial existe dentro de cada Pedido;\n"
                           "no hay una instancia global para mostrar aquí)")
        elif est == "Lista Circular":
            reps = self.lista_repartidores.recorrer()
            if reps:
                actual = self.lista_repartidores.actual()
                lineas = ["ListaCircular de repartidores:\n"]
                for r in reps:
                    marca = " ← turno actual" if r == actual else ""
                    lineas.append(f"  {r}{marca}")
                self._escribir("\n".join(lineas))
            else:
                self._escribir("(sin repartidores)")
        elif est == "Pila Estática":
            from estructuras.pila import PilaEstatica
            p = PilaEstatica(5)
            for v in [10, 20, 30]:
                p.apilar(v)
            self._escribir(
                "Ejemplo PilaEstatica(cap=5):\n"
                f"  Contenido: {[p._datos[i] for i in range(p._tope + 1)]}\n"
                f"  Tope: {p.ver_tope()}\n"
                f"  Longitud: {p.longitud()}"
            )
        elif est == "Pila Dinámica":
            self._escribir(
                "(la PilaDinamica vive dentro de cada Pedido como _cargados;\n"
                "no hay instancia global para mostrar aquí)"
            )
        elif est == "Cola Simple":
            pedidos = self.cola_pedidos.obtener_todos()
            if pedidos:
                lineas = ["ColaSimple (pedidos normales):\n"]
                for p in pedidos:
                    lineas.append(f"  {p}")
                self._escribir("\n".join(lineas))
            else:
                self._escribir("ColaSimple vacía (no hay pedidos normales en espera).")
        elif est == "Cola Circular":
            recientes = self.cola_recientes.obtener_todos()
            if recientes:
                lineas = [f"ColaCircular(cap={self.cola_recientes.capacidad}) — últimos despachados:\n"]
                for p in recientes:
                    lineas.append(f"  {p}")
                self._escribir("\n".join(lineas))
            else:
                self._escribir("ColaCircular vacía (aún no se despachó ningún pedido).")
        elif est == "Cola Prioridad":
            urg = self.cola_urgentes.obtener_todos()
            if urg:
                lineas = ["ColaPrioridad (pedidos urgentes):\n"]
                for p in urg:
                    lineas.append(f"  ⚡ {p}")
                self._escribir("\n".join(lineas))
            else:
                self._escribir("ColaPrioridad vacía (no hay pedidos urgentes en espera).")
        elif est in ("ABB", "AVL"):
            productos = self.catalogo.inorden()
            lineas = [f"{est} — inorden del catálogo:\n"]
            for p in productos:
                lineas.append(f"  [{p.codigo:3}] {p.nombre:<25} ${p.precio:.2f}")
            lineas.append(f"\nTotal de nodos: {len(productos)}")
            lineas.append("\nRepresentación del árbol (rotado 90°, raíz a la izquierda):\n")
            lineas.append(repr(self.catalogo))
            self._escribir("\n".join(lineas))
        elif est == "Grafo":
            from estructuras.grafo import GrafoLista
            lineas = ["GrafoLista — lista de adyacencia:\n"]
            for v in self.catalogo.__class__.__mro__:
                pass   # sólo para que no quede vacío
            # acceder al grafo a través del catalogo no tiene sentido; mostrar texto fijo
            lineas = [
                "Grafo de zonas (GrafoLista):\n",
                "  Local     → [Norte, Sur]",
                "  Norte     → [Local, Costanera]",
                "  Sur       → [Local, Costanera]",
                "  Costanera → [Norte, Sur, Isla]",
                "  Isla      → [Costanera]",
            ]
            self._escribir("\n".join(lineas))

    def _mostrar_recorrido(self, tipo):
        est = self._var_est.get()
        if est not in ("ABB", "AVL"):
            self._escribir(f"Los recorridos (inorden/preorden/postorden) solo aplican a ABB/AVL.\nEstructura seleccionada: {est}")
            return
        if tipo == "inorden":
            productos = self.catalogo.inorden()
            titulo = "Inorden (ascendente por código):"
        elif tipo == "preorden":
            productos = self.catalogo.preorden()
            titulo = "Preorden (raíz, izquierda, derecha):"
        else:
            productos = self.catalogo.postorden()
            titulo = "Postorden (izquierda, derecha, raíz):"

        lineas = [f"{titulo}\n"]
        for p in productos:
            lineas.append(f"  [{p.codigo:3}] {p.nombre}")
        self._escribir("\n".join(lineas))
