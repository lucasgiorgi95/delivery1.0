"""
Panel Nuevo Pedido — crea pedidos con ítems, combos y pila de deshacer.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modelos import Pedido, ItemPedido, Combo


class PanelPedidos(ttk.Frame):
    """Pestaña 'Nuevo Pedido': arma y confirma pedidos."""

    ZONAS = ["Norte", "Sur", "Costanera", "Isla"]

    def __init__(self, parent, catalogo, cola_pedidos, cola_urgentes, **kwargs):
        super().__init__(parent, **kwargs)
        self.catalogo = catalogo
        self.cola_pedidos = cola_pedidos
        self.cola_urgentes = cola_urgentes
        self._pedido_actual = None
        self._items_combo_pendiente = []   # ítems seleccionados para armar combo
        self._construir_ui()

    # ─────────────────────────────────────────────
    # Construcción de la interfaz
    # ─────────────────────────────────────────────

    def _construir_ui(self):
        self.configure(padding=8)

        # Título
        ttk.Label(self, text="Nuevo Pedido",
                  font=("Segoe UI", 12, "bold")).grid(
                      row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        # ── Columna izquierda ──────────────────────
        frm_izq = ttk.Frame(self)
        frm_izq.grid(row=1, column=0, sticky="nsew", padx=(0, 6))

        self._construir_datos_cliente(frm_izq)
        self._construir_agregar_productos(frm_izq)
        self._construir_combo(frm_izq)
        self._construir_confirmar(frm_izq)

        # ── Columna derecha ────────────────────────
        frm_der = ttk.Frame(self)
        frm_der.grid(row=1, column=1, sticky="nsew")

        self._construir_preview(frm_der)
        self._construir_historial(frm_der)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Poblar los combobox de productos DESPUÉS de que todos los widgets existan
        self._actualizar_combo_productos()

    # ── sección datos del cliente ──────────────

    def _construir_datos_cliente(self, parent):
        frm = ttk.LabelFrame(parent, text="Datos del cliente", padding=8)
        frm.pack(fill="x", pady=(0, 6))

        ttk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky="e", pady=3, padx=4)
        self._var_cliente = tk.StringVar()
        ttk.Entry(frm, textvariable=self._var_cliente, width=28).grid(
            row=0, column=1, columnspan=2, pady=3, sticky="w")

        ttk.Label(frm, text="Tipo entrega:").grid(row=1, column=0, sticky="e", padx=4)
        self._var_tipo = tk.StringVar(value="Retira en local")
        cb_tipo = ttk.Combobox(frm, textvariable=self._var_tipo, width=20,
                               values=["Retira en local", "Delivery a domicilio"],
                               state="readonly")
        cb_tipo.grid(row=1, column=1, sticky="w", pady=3)
        cb_tipo.bind("<<ComboboxSelected>>", self._toggle_zona)

        ttk.Label(frm, text="Zona destino:").grid(row=2, column=0, sticky="e", padx=4)
        self._var_zona = tk.StringVar()
        self._cb_zona = ttk.Combobox(frm, textvariable=self._var_zona, width=15,
                                     values=self.ZONAS, state="disabled")
        self._cb_zona.grid(row=2, column=1, sticky="w", pady=3)

    # ── sección agregar productos ──────────────

    def _construir_agregar_productos(self, parent):
        frm = ttk.LabelFrame(parent, text="Agregar productos al pedido", padding=8)
        frm.pack(fill="x", pady=(0, 6))

        ttk.Label(frm, text="Producto:").grid(row=0, column=0, sticky="e", padx=4, pady=3)
        self._var_prod = tk.StringVar()
        self._cb_prod = ttk.Combobox(frm, textvariable=self._var_prod, width=34,
                                     state="readonly")
        self._cb_prod.grid(row=0, column=1, columnspan=2, pady=3, sticky="w")

        ttk.Label(frm, text="Cantidad:").grid(row=1, column=0, sticky="e", padx=4)
        self._var_cant = tk.StringVar(value="1")
        ttk.Spinbox(frm, textvariable=self._var_cant, from_=1, to=99, width=5).grid(
            row=1, column=1, sticky="w", pady=3)

        frm_btns = ttk.Frame(frm)
        frm_btns.grid(row=2, column=0, columnspan=3, sticky="w", pady=(4, 0))
        ttk.Button(frm_btns, text="+ Agregar al pedido",
                   command=self._agregar_item).pack(side="left", padx=(0, 4))
        ttk.Button(frm_btns, text="↩ Quitar último",
                   command=self._quitar_ultimo).pack(side="left")

    # ── sección combo ──────────────────────────

    def _construir_combo(self, parent):
        frm = ttk.LabelFrame(parent, text="Armar Combo", padding=8)
        frm.pack(fill="x", pady=(0, 6))

        ttk.Label(frm, text="Nombre combo:").grid(row=0, column=0, sticky="e", padx=4, pady=3)
        self._var_nom_combo = tk.StringVar()
        ttk.Entry(frm, textvariable=self._var_nom_combo, width=22).grid(
            row=0, column=1, sticky="w", pady=3)

        ttk.Label(frm, text="Descuento %:").grid(row=1, column=0, sticky="e", padx=4)
        self._var_desc = tk.StringVar(value="10")
        ttk.Spinbox(frm, textvariable=self._var_desc, from_=0, to=50, width=5).grid(
            row=1, column=1, sticky="w", pady=3)

        ttk.Label(frm, text="Ítem a incluir:").grid(row=2, column=0, sticky="e", padx=4)
        self._var_item_combo = tk.StringVar()
        self._cb_item_combo = ttk.Combobox(frm, textvariable=self._var_item_combo,
                                           width=28, state="readonly")
        self._cb_item_combo.grid(row=2, column=1, sticky="w", pady=3)

        frm_btns = ttk.Frame(frm)
        frm_btns.grid(row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))
        ttk.Button(frm_btns, text="+ Ítem al combo",
                   command=self._agregar_item_combo).pack(side="left", padx=(0, 4))
        ttk.Button(frm_btns, text="✔ Crear Combo",
                   command=self._crear_combo).pack(side="left")

        # ítems seleccionados para el combo
        ttk.Label(frm, text="Ítems del combo:").grid(row=4, column=0, sticky="ne", padx=4, pady=3)
        self._lst_combo_items = tk.Listbox(frm, height=4, width=34)
        self._lst_combo_items.grid(row=4, column=1, sticky="w", pady=3)

    # ── sección confirmar ──────────────────────

    def _construir_confirmar(self, parent):
        frm = ttk.LabelFrame(parent, text="Confirmar pedido", padding=8)
        frm.pack(fill="x")

        self._var_urgente = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm, text="Pedido URGENTE",
                        variable=self._var_urgente).pack(anchor="w")

        frm_btns = ttk.Frame(frm)
        frm_btns.pack(pady=(6, 0))
        ttk.Button(frm_btns, text="✔ Confirmar Pedido",
                   command=self._confirmar).pack(side="left", padx=(0, 8))
        ttk.Button(frm_btns, text="✖ Limpiar",
                   command=self._limpiar).pack(side="left")

    # ── preview y historial ────────────────────

    def _construir_preview(self, parent):
        frm = ttk.LabelFrame(parent, text="Vista previa del pedido", padding=8)
        frm.pack(fill="both", expand=True, pady=(0, 6))

        self._lst_preview = tk.Listbox(frm, height=12, width=42,
                                       font=("Courier New", 9))
        scroll = ttk.Scrollbar(frm, orient="vertical", command=self._lst_preview.yview)
        self._lst_preview.configure(yscrollcommand=scroll.set)
        self._lst_preview.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._lbl_total = ttk.Label(frm, text="Total: $0.00",
                                    font=("Segoe UI", 11, "bold"))
        self._lbl_total.pack(anchor="e", pady=(4, 0))

        self._lbl_combos = ttk.Label(frm, text="", foreground="#6a1b9a")
        self._lbl_combos.pack(anchor="w")

    def _construir_historial(self, parent):
        frm = ttk.LabelFrame(parent, text="Historial de estados (Lista Doble)", padding=8)
        frm.pack(fill="x")

        self._txt_historial = tk.Text(frm, height=5, width=42,
                                      font=("Courier New", 9), state="disabled",
                                      background="#f9fbe7")
        self._txt_historial.pack(fill="x")

    # ─────────────────────────────────────────────
    # Lógica
    # ─────────────────────────────────────────────

    def _actualizar_combo_productos(self):
        productos = self.catalogo.inorden()
        opciones = [f"{p.codigo} - {p.nombre} - ${p.precio:.2f}" for p in productos]
        self._cb_prod["values"] = opciones
        self._cb_item_combo["values"] = opciones
        if opciones:
            self._cb_prod.set(opciones[0])
            self._cb_item_combo.set(opciones[0])

    def _toggle_zona(self, _event=None):
        if self._var_tipo.get() == "Delivery a domicilio":
            self._cb_zona.config(state="readonly")
        else:
            self._cb_zona.config(state="disabled")
            self._var_zona.set("")

    def _obtener_o_crear_pedido(self):
        if self._pedido_actual is None:
            tipo = "delivery" if self._var_tipo.get() == "Delivery a domicilio" else "retira"
            cliente = self._var_cliente.get().strip() or "Sin nombre"
            self._pedido_actual = Pedido(cliente, tipo)
        return self._pedido_actual

    def _producto_desde_seleccion(self, texto):
        """Extrae el código del combo y busca el producto en el AVL."""
        cod_str = texto.split(" - ")[0].strip()
        try:
            cod = int(cod_str)
        except ValueError:
            return None
        return self.catalogo.buscar(cod)

    def _agregar_item(self):
        seleccion = self._var_prod.get()
        if not seleccion:
            messagebox.showerror("Error", "Seleccioná un producto.")
            return
        try:
            cant = int(self._var_cant.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a 0.")
            return

        producto = self._producto_desde_seleccion(seleccion)
        if producto is None:
            messagebox.showerror("Error", "No se pudo encontrar el producto.")
            return

        pedido = self._obtener_o_crear_pedido()
        item = ItemPedido(producto, cant)
        pedido.agregar_item(item)
        self._refrescar_preview()

    def _quitar_ultimo(self):
        if self._pedido_actual is None:
            return
        item = self._pedido_actual.quitar_ultimo()
        if item:
            self._refrescar_preview()
        else:
            messagebox.showinfo("Info", "No hay ítems para quitar.")

    def _agregar_item_combo(self):
        seleccion = self._var_item_combo.get()
        if not seleccion:
            messagebox.showerror("Error", "Seleccioná un producto para el combo.")
            return
        try:
            cant = int(self._var_cant.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            cant = 1

        producto = self._producto_desde_seleccion(seleccion)
        if producto is None:
            return
        item = ItemPedido(producto, cant)
        self._items_combo_pendiente.append(item)
        self._lst_combo_items.insert("end", str(item))

    def _crear_combo(self):
        if not self._items_combo_pendiente:
            messagebox.showerror("Error", "Agregá al menos un ítem al combo.")
            return
        nom = self._var_nom_combo.get().strip()
        if not nom:
            messagebox.showerror("Error", "Escribí un nombre para el combo.")
            return
        try:
            desc = float(self._var_desc.get()) / 100.0
        except ValueError:
            desc = 0.10

        pedido = self._obtener_o_crear_pedido()
        combo = Combo(nom, list(self._items_combo_pendiente), descuento=desc)
        pedido.agregar_combo(combo)

        # limpiar selección de combo
        self._items_combo_pendiente.clear()
        self._lst_combo_items.delete(0, "end")
        self._var_nom_combo.set("")
        self._refrescar_preview()
        messagebox.showinfo("Combo creado", f"Combo '{nom}' agregado al pedido.")

    def _refrescar_preview(self):
        if self._pedido_actual is None:
            return
        self._lst_preview.delete(0, "end")
        # ítems individuales
        nodo = self._pedido_actual.items.cabeza
        while nodo:
            self._lst_preview.insert("end", str(nodo.dato))
            nodo = nodo.siguiente
        # combos
        for combo in self._pedido_actual.combos:
            self._lst_preview.insert("end", f"  ► {combo}")
        # total
        self._lbl_total.config(text=f"Total: ${self._pedido_actual.total():.2f}")
        # combos activos
        n_combos = len(self._pedido_actual.combos)
        if n_combos:
            self._lbl_combos.config(text=f"Combos activos: {n_combos}")
        else:
            self._lbl_combos.config(text="")
        # historial
        estados = self._pedido_actual.historial.recorrer()
        self._txt_historial.config(state="normal")
        self._txt_historial.delete("1.0", "end")
        for est in estados:
            self._txt_historial.insert("end", f"  → {est}\n")
        self._txt_historial.config(state="disabled")

    def _confirmar(self):
        cliente = self._var_cliente.get().strip()
        if not cliente:
            messagebox.showerror("Error", "El nombre del cliente no puede estar vacío.")
            return

        tipo = "delivery" if self._var_tipo.get() == "Delivery a domicilio" else "retira"
        if tipo == "delivery" and not self._var_zona.get():
            messagebox.showerror("Error", "Seleccioná la zona de destino para el delivery.")
            return

        if self._pedido_actual is None:
            messagebox.showerror("Error", "El pedido está vacío. Agregá al menos un ítem.")
            return

        pedido = self._pedido_actual
        # sincronizar cliente y tipo por si se cambió después de crear el pedido
        pedido.cliente = cliente
        pedido.tipo_entrega = tipo
        pedido.zona_destino = self._var_zona.get() if tipo == "delivery" else None

        items_lista = pedido.items.recorrer()
        if not items_lista and not pedido.combos:
            messagebox.showerror("Error", "El pedido no tiene ítems ni combos.")
            return

        pedido.urgente = self._var_urgente.get()
        pedido.cambiar_estado("confirmado")

        if pedido.urgente:
            self.cola_urgentes.encolar(pedido, prioridad=0)
        else:
            self.cola_pedidos.encolar(pedido)

        messagebox.showinfo(
            "Pedido confirmado",
            f"{pedido}\nTotal: ${pedido.total():.2f}\n"
            f"Encolado como {'URGENTE' if pedido.urgente else 'normal'}."
        )
        self._limpiar()

    def _limpiar(self):
        self._pedido_actual = None
        self._items_combo_pendiente.clear()
        self._var_cliente.set("")
        self._var_tipo.set("Retira en local")
        self._var_zona.set("")
        self._cb_zona.config(state="disabled")
        self._var_cant.set("1")
        self._var_nom_combo.set("")
        self._var_desc.set("10")
        self._var_urgente.set(False)
        self._lst_preview.delete(0, "end")
        self._lst_combo_items.delete(0, "end")
        self._lbl_total.config(text="Total: $0.00")
        self._lbl_combos.config(text="")
        self._txt_historial.config(state="normal")
        self._txt_historial.delete("1.0", "end")
        self._txt_historial.config(state="disabled")
        self._actualizar_combo_productos()
