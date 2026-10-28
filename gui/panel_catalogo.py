"""
Panel Catálogo — muestra el AVL de productos en un Treeview.
Permite buscar por código, agregar y eliminar productos.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modelos import Producto


class PanelCatalogo(ttk.Frame):
    """Pestaña 'Catálogo': explora el árbol AVL de productos."""

    def __init__(self, parent, catalogo, **kwargs):
        super().__init__(parent, **kwargs)
        self.catalogo = catalogo   # instancia de AVL
        self._construir_ui()
        self.actualizar_catalogo()

    # ─────────────────────────────────────────────
    # Construcción de la interfaz
    # ─────────────────────────────────────────────

    def _construir_ui(self):
        self.configure(padding=10)

        # Título
        lbl_titulo = ttk.Label(
            self, text="Catálogo de Productos — Árbol AVL  (búsqueda O(log n))",
            font=("Segoe UI", 12, "bold")
        )
        lbl_titulo.pack(anchor="w", pady=(0, 8))

        # ── Barra de herramientas ──────────────────
        frm_toolbar = ttk.Frame(self)
        frm_toolbar.pack(fill="x", pady=(0, 6))

        ttk.Button(frm_toolbar, text="↻ Actualizar catálogo",
                   command=self.actualizar_catalogo).pack(side="left", padx=(0, 4))

        ttk.Separator(frm_toolbar, orient="vertical").pack(side="left", fill="y", padx=6)

        # Buscar
        ttk.Label(frm_toolbar, text="Buscar código:").pack(side="left")
        self._var_buscar = tk.StringVar()
        ttk.Entry(frm_toolbar, textvariable=self._var_buscar, width=8).pack(side="left", padx=4)
        ttk.Button(frm_toolbar, text="Buscar", command=self._buscar).pack(side="left", padx=(0, 10))

        # Eliminar
        ttk.Label(frm_toolbar, text="Eliminar código:").pack(side="left")
        self._var_eliminar = tk.StringVar()
        ttk.Entry(frm_toolbar, textvariable=self._var_eliminar, width=8).pack(side="left", padx=4)
        ttk.Button(frm_toolbar, text="Eliminar", command=self._eliminar).pack(side="left")

        # ── Treeview ──────────────────────────────
        frm_tree = ttk.Frame(self)
        frm_tree.pack(fill="both", expand=True, pady=(0, 8))

        cols = ("codigo", "nombre", "precio", "categoria")
        self._tree = ttk.Treeview(frm_tree, columns=cols, show="headings", height=14)
        self._tree.heading("codigo",    text="Código")
        self._tree.heading("nombre",    text="Nombre")
        self._tree.heading("precio",    text="Precio")
        self._tree.heading("categoria", text="Categoría")
        self._tree.column("codigo",    width=70,  anchor="center")
        self._tree.column("nombre",    width=200)
        self._tree.column("precio",    width=90,  anchor="e")
        self._tree.column("categoria", width=100, anchor="center")

        scroll = ttk.Scrollbar(frm_tree, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scroll.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # ── Formulario de alta ────────────────────
        frm_alta = ttk.LabelFrame(self, text="Agregar producto al catálogo", padding=8)
        frm_alta.pack(fill="x")

        campos = ttk.Frame(frm_alta)
        campos.pack(fill="x")

        ttk.Label(campos, text="Código:").grid(row=0, column=0, sticky="e", padx=4, pady=3)
        self._var_cod   = tk.StringVar()
        ttk.Entry(campos, textvariable=self._var_cod, width=8).grid(row=0, column=1, pady=3)

        ttk.Label(campos, text="Nombre:").grid(row=0, column=2, sticky="e", padx=4)
        self._var_nom   = tk.StringVar()
        ttk.Entry(campos, textvariable=self._var_nom, width=22).grid(row=0, column=3, pady=3)

        ttk.Label(campos, text="Precio:").grid(row=0, column=4, sticky="e", padx=4)
        self._var_pre   = tk.StringVar()
        ttk.Entry(campos, textvariable=self._var_pre, width=10).grid(row=0, column=5, pady=3)

        ttk.Label(campos, text="Categoría:").grid(row=0, column=6, sticky="e", padx=4)
        self._var_cat   = tk.StringVar(value="comida")
        ttk.Combobox(campos, textvariable=self._var_cat, width=9,
                     values=["comida", "bebida"],
                     state="readonly").grid(row=0, column=7, pady=3)

        ttk.Button(frm_alta, text="Agregar producto",
                   command=self._agregar_producto).pack(anchor="e", pady=(6, 0))

        # Mensaje de estado
        self._lbl_estado = ttk.Label(self, text="", foreground="#2e7d32")
        self._lbl_estado.pack(anchor="w")

    # ─────────────────────────────────────────────
    # Lógica
    # ─────────────────────────────────────────────

    def actualizar_catalogo(self):
        """Recorre el AVL en inorden y rellena el Treeview."""
        for row in self._tree.get_children():
            self._tree.delete(row)
        productos = self.catalogo.inorden()
        for p in productos:
            self._tree.insert("", "end", values=(
                p.codigo, p.nombre, f"${p.precio:.2f}", p.categoria
            ))
        self._lbl_estado.config(
            text=f"Catálogo actualizado — {len(productos)} productos en el AVL."
        )

    def _buscar(self):
        cod_str = self._var_buscar.get().strip()
        if not cod_str:
            messagebox.showerror("Error", "Ingresá un código para buscar.")
            return
        try:
            cod = int(cod_str)
        except ValueError:
            messagebox.showerror("Error", "El código debe ser un número entero.")
            return
        producto = self.catalogo.buscar(cod)
        if producto:
            # Resaltar en el treeview
            for item in self._tree.get_children():
                vals = self._tree.item(item, "values")
                if int(vals[0]) == cod:
                    self._tree.selection_set(item)
                    self._tree.see(item)
                    break
            self._lbl_estado.config(
                text=f"✔ Encontrado: {producto}",
                foreground="#1565c0"
            )
        else:
            self._lbl_estado.config(
                text=f"✘ No se encontró el código {cod}.",
                foreground="#c62828"
            )

    def _eliminar(self):
        cod_str = self._var_eliminar.get().strip()
        if not cod_str:
            messagebox.showerror("Error", "Ingresá un código para eliminar.")
            return
        try:
            cod = int(cod_str)
        except ValueError:
            messagebox.showerror("Error", "El código debe ser un número entero.")
            return
        producto = self.catalogo.buscar(cod)
        if not producto:
            messagebox.showerror("Error", f"No existe producto con código {cod}.")
            return
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar '{producto.nombre}' del catálogo?"
        )
        if confirmar:
            self.catalogo.eliminar(cod)
            self._var_eliminar.set("")
            self.actualizar_catalogo()
            self._lbl_estado.config(
                text=f"Producto {cod} eliminado del AVL.",
                foreground="#e65100"
            )

    def _agregar_producto(self):
        cod_str = self._var_cod.get().strip()
        nom     = self._var_nom.get().strip()
        pre_str = self._var_pre.get().strip()
        cat     = self._var_cat.get().strip()

        if not cod_str or not nom or not pre_str:
            messagebox.showerror("Error", "Completá todos los campos (código, nombre, precio).")
            return
        try:
            cod = int(cod_str)
        except ValueError:
            messagebox.showerror("Error", "El código debe ser un número entero.")
            return
        try:
            pre = float(pre_str)
            if pre <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número mayor a 0.")
            return
        if cat not in ("comida", "bebida"):
            messagebox.showerror("Error", "La categoría debe ser 'comida' o 'bebida'.")
            return

        nuevo = Producto(cod, nom, pre, cat)
        self.catalogo.insertar(cod, nuevo)
        self._var_cod.set("")
        self._var_nom.set("")
        self._var_pre.set("")
        self.actualizar_catalogo()
        self._lbl_estado.config(
            text=f"✔ Producto [{cod}] {nom} agregado al AVL.",
            foreground="#2e7d32"
        )
