"""
Panel Zonas — visualiza el grafo de zonas y ejecuta BFS / DFS.
"""

import tkinter as tk
from tkinter import ttk, messagebox


# Coordenadas fijas para cada zona en el canvas
POSICIONES = {
    "Local":     (200, 200),
    "Norte":     (200, 80),
    "Sur":       (200, 320),
    "Costanera": (360, 200),
    "Isla":      (500, 200),
}

RADIO = 30
COLOR_NODO       = "#1565c0"
COLOR_NODO_HOVER = "#42a5f5"
COLOR_ARISTA     = "#90a4ae"
COLOR_RUTA       = "#e53935"
COLOR_TEXTO      = "white"


class PanelZonas(ttk.Frame):
    """Pestaña 'Zonas': grafo de delivery con BFS y DFS."""

    def __init__(self, parent, grafo_zonas, **kwargs):
        super().__init__(parent, **kwargs)
        self.grafo = grafo_zonas
        self._ruta_activa = []
        self._construir_ui()
        self._dibujar_grafo()

    # ─────────────────────────────────────────────
    # Construcción de la interfaz
    # ─────────────────────────────────────────────

    def _construir_ui(self):
        self.configure(padding=10)

        ttk.Label(self, text="Mapa de Zonas de Delivery — Grafo con BFS y DFS",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

        # ── Fila principal ─────────────────────────
        frm_main = ttk.Frame(self)
        frm_main.pack(fill="both", expand=True)

        # Canvas del grafo
        self._canvas = tk.Canvas(frm_main, width=580, height=400,
                                 bg="#eceff1", relief="sunken", bd=1)
        self._canvas.pack(side="left", padx=(0, 10))

        # Panel derecho
        frm_der = ttk.Frame(frm_main)
        frm_der.pack(side="left", fill="both", expand=True)

        frm_ctrl = ttk.LabelFrame(frm_der, text="Controles", padding=8)
        frm_ctrl.pack(fill="x", pady=(0, 8))

        ttk.Label(frm_ctrl, text="Zona destino:").pack(anchor="w")
        zonas = self.grafo.obtener_vertices()
        self._var_destino = tk.StringVar(
            value=zonas[1] if len(zonas) > 1 else (zonas[0] if zonas else "")
        )
        self._cb_destino = ttk.Combobox(frm_ctrl, textvariable=self._var_destino,
                                        values=zonas, state="readonly", width=16)
        self._cb_destino.pack(anchor="w", pady=4)

        ttk.Button(frm_ctrl, text="BFS — Ruta más corta",
                   command=self._ejecutar_bfs).pack(fill="x", pady=2)
        ttk.Button(frm_ctrl, text="DFS — Zonas alcanzables",
                   command=self._ejecutar_dfs).pack(fill="x", pady=2)
        ttk.Button(frm_ctrl, text="Limpiar resaltado",
                   command=self._limpiar_resaltado).pack(fill="x", pady=(8, 2))

        # Resultado
        frm_res = ttk.LabelFrame(frm_der, text="Resultado del recorrido", padding=8)
        frm_res.pack(fill="both", expand=True)

        self._txt_res = tk.Text(frm_res, height=14, width=30,
                                font=("Courier New", 9), state="disabled",
                                background="#f9fbe7")
        sc = ttk.Scrollbar(frm_res, orient="vertical", command=self._txt_res.yview)
        self._txt_res.configure(yscrollcommand=sc.set)
        self._txt_res.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

    # ─────────────────────────────────────────────
    # Dibujo del grafo
    # ─────────────────────────────────────────────

    def _dibujar_grafo(self, ruta=None):
        """Redibuja el grafo completo. Si se pasa una ruta, la resalta en rojo."""
        self._canvas.delete("all")
        ruta_set = set()
        ruta_aristas = set()
        if ruta:
            ruta_set = set(ruta)
            for i in range(len(ruta) - 1):
                arista = frozenset([ruta[i], ruta[i + 1]])
                ruta_aristas.add(arista)

        # Dibujar aristas
        for v in self.grafo.obtener_vertices():
            x1, y1 = POSICIONES.get(v, (0, 0))
            for w in self.grafo.obtener_vecinos(v):
                x2, y2 = POSICIONES.get(w, (0, 0))
                arista = frozenset([v, w])
                color = COLOR_RUTA if arista in ruta_aristas else COLOR_ARISTA
                ancho = 3 if arista in ruta_aristas else 1
                self._canvas.create_line(x1, y1, x2, y2,
                                         fill=color, width=ancho)

        # Dibujar nodos
        for nombre, (cx, cy) in POSICIONES.items():
            color = COLOR_RUTA if nombre in ruta_set else COLOR_NODO
            self._canvas.create_oval(cx - RADIO, cy - RADIO,
                                     cx + RADIO, cy + RADIO,
                                     fill=color, outline="white", width=2)
            self._canvas.create_text(cx, cy, text=nombre,
                                     fill=COLOR_TEXTO,
                                     font=("Segoe UI", 9, "bold"))

        # Leyenda
        self._canvas.create_text(10, 390, anchor="sw",
                                  text="● Local (origen)  — BFS: ruta más corta  — DFS: profundidad",
                                  font=("Segoe UI", 8), fill="#546e7a")

    # ─────────────────────────────────────────────
    # Acciones
    # ─────────────────────────────────────────────

    def _ejecutar_bfs(self):
        destino = self._var_destino.get()
        if not destino:
            messagebox.showerror("Error", "Seleccioná una zona destino.")
            return

        camino = self.grafo.bfs("Local", destino)

        self._txt_res.config(state="normal")
        self._txt_res.delete("1.0", "end")

        if camino:
            self._txt_res.insert("end", "BFS — Ruta más corta:\n\n")
            self._txt_res.insert("end", " → ".join(camino) + "\n\n")
            self._txt_res.insert("end", f"Paradas: {len(camino) - 1}\n")
            self._dibujar_grafo(ruta=camino)
        else:
            self._txt_res.insert("end", f"No hay ruta hacia {destino}.\n")
            self._dibujar_grafo()

        self._txt_res.config(state="disabled")

    def _ejecutar_dfs(self):
        zonas = self.grafo.dfs("Local")

        self._txt_res.config(state="normal")
        self._txt_res.delete("1.0", "end")
        self._txt_res.insert("end", "DFS — Zonas alcanzables desde Local:\n\n")
        for i, z in enumerate(zonas, 1):
            self._txt_res.insert("end", f"  {i}. {z}\n")
        self._txt_res.insert("end", f"\nTotal: {len(zonas)} zonas alcanzadas.\n")
        self._txt_res.config(state="disabled")

        self._dibujar_grafo(ruta=zonas)

    def _limpiar_resaltado(self):
        self._txt_res.config(state="normal")
        self._txt_res.delete("1.0", "end")
        self._txt_res.config(state="disabled")
        self._dibujar_grafo()
