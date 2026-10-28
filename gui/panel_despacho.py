"""
Panel Despacho — gestiona las colas de pedidos y el repartidor de turno.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class PanelDespacho(ttk.Frame):
    """
    Pestaña 'Despacho':
      - Muestra pedidos normales (ColaSimple) y urgentes (ColaPrioridad).
      - Botón 'Despachar siguiente' extrae de urgentes primero.
      - Muestra los últimos 3 despachados (ColaCircular).
      - Muestra el repartidor de turno (ListaCircular).
    """

    def __init__(self, parent, cola_pedidos, cola_urgentes,
                 cola_recientes, lista_repartidores, **kwargs):
        super().__init__(parent, **kwargs)
        self.cola_pedidos       = cola_pedidos
        self.cola_urgentes      = cola_urgentes
        self.cola_recientes     = cola_recientes
        self.lista_repartidores = lista_repartidores
        self._construir_ui()
        self.actualizar()

    # ─────────────────────────────────────────────
    # Construcción de la interfaz
    # ─────────────────────────────────────────────

    def _construir_ui(self):
        self.configure(padding=10)

        ttk.Label(self, text="Panel de Despacho",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

        # ── Fila superior: colas ───────────────────
        frm_colas = ttk.Frame(self)
        frm_colas.pack(fill="both", expand=True, pady=(0, 8))
        frm_colas.columnconfigure(0, weight=1)
        frm_colas.columnconfigure(1, weight=1)

        # Cola normal
        frm_normal = ttk.LabelFrame(frm_colas, text="Cola Normal (FIFO — ColaSimple)", padding=8)
        frm_normal.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self._lst_normal = tk.Listbox(frm_normal, height=10,
                                      font=("Courier New", 9), selectmode="browse")
        sc_n = ttk.Scrollbar(frm_normal, orient="vertical", command=self._lst_normal.yview)
        self._lst_normal.configure(yscrollcommand=sc_n.set)
        self._lst_normal.pack(side="left", fill="both", expand=True)
        sc_n.pack(side="right", fill="y")

        # Cola urgentes
        frm_urg = ttk.LabelFrame(frm_colas,
                                 text="Cola Urgentes (Heap Mínimo — ColaPrioridad)", padding=8)
        frm_urg.grid(row=0, column=1, sticky="nsew")
        self._lst_urgentes = tk.Listbox(frm_urg, height=10,
                                        font=("Courier New", 9),
                                        background="#fff3e0", selectmode="browse")
        sc_u = ttk.Scrollbar(frm_urg, orient="vertical", command=self._lst_urgentes.yview)
        self._lst_urgentes.configure(yscrollcommand=sc_u.set)
        self._lst_urgentes.pack(side="left", fill="both", expand=True)
        sc_u.pack(side="right", fill="y")

        # ── Botón despachar ────────────────────────
        frm_btn = ttk.Frame(self)
        frm_btn.pack(pady=4)
        ttk.Button(frm_btn, text="🚀  Despachar siguiente",
                   command=self._despachar).pack(side="left", padx=(0, 10))
        ttk.Button(frm_btn, text="↻ Actualizar",
                   command=self.actualizar).pack(side="left")

        # ── Repartidor de turno ────────────────────
        frm_rep = ttk.LabelFrame(self, text="Repartidor de turno (ListaCircular)", padding=8)
        frm_rep.pack(fill="x", pady=(0, 6))

        self._lbl_repartidor = ttk.Label(
            frm_rep, text="—", font=("Segoe UI", 13, "bold"), foreground="#1565c0"
        )
        self._lbl_repartidor.pack(side="left", padx=8)

        # ── Últimos 3 despachados ──────────────────
        frm_rec = ttk.LabelFrame(self,
                                 text="Últimos 3 despachados (ColaCircular)", padding=8)
        frm_rec.pack(fill="x")

        self._lst_recientes = tk.Listbox(frm_rec, height=4,
                                         font=("Courier New", 9),
                                         background="#e8f5e9")
        self._lst_recientes.pack(fill="x")

    # ─────────────────────────────────────────────
    # Lógica
    # ─────────────────────────────────────────────

    def actualizar(self):
        """Refresca todos los widgets con el estado actual de las colas."""
        # Cola normal
        self._lst_normal.delete(0, "end")
        for p in self.cola_pedidos.obtener_todos():
            self._lst_normal.insert("end", f"  #{p.numero}  {p.cliente}  ${p.total():.2f}")

        # Cola urgentes
        self._lst_urgentes.delete(0, "end")
        for p in self.cola_urgentes.obtener_todos():
            self._lst_urgentes.insert("end", f"  ⚡ #{p.numero}  {p.cliente}  ${p.total():.2f}")

        # Repartidor de turno
        rep = self.lista_repartidores.actual()
        self._lbl_repartidor.config(
            text=f"Próximo: {rep}" if rep else "Sin repartidores"
        )

        # Últimos despachados
        self._lst_recientes.delete(0, "end")
        for p in self.cola_recientes.obtener_todos():
            self._lst_recientes.insert(
                "end", f"  ✔ #{p.numero}  {p.cliente}  {p.estado}")

    def _despachar(self):
        pedido = None
        fuente = ""
        # Urgentes primero
        if not self.cola_urgentes.esta_vacia():
            pedido = self.cola_urgentes.desencolar()
            fuente = "urgentes"
        elif not self.cola_pedidos.esta_vacia():
            pedido = self.cola_pedidos.desencolar()
            fuente = "normal"

        if pedido is None:
            messagebox.showinfo("Sin pedidos", "No hay pedidos en espera.")
            return

        pedido.cambiar_estado("despachado")
        self.cola_recientes.encolar(pedido)
        self.lista_repartidores.siguiente_turno()   # rotar repartidor

        messagebox.showinfo(
            "Pedido despachado",
            f"{pedido}\nCola de origen: {fuente}\n"
            f"Repartidor: {self.lista_repartidores.actual()}"
        )
        self.actualizar()
