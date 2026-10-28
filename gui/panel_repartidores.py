"""
Panel Repartidores — gestiona la lista circular de repartidores.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class PanelRepartidores(ttk.Frame):
    """Pestaña 'Repartidores': administra la lista circular de turnos."""

    def __init__(self, parent, lista_repartidores, **kwargs):
        super().__init__(parent, **kwargs)
        self.lista = lista_repartidores
        self._construir_ui()
        self._refrescar()

    # ─────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────

    def _construir_ui(self):
        self.configure(padding=14)

        ttk.Label(self, text="Gestión de Repartidores — Lista Circular",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # ── Turno actual ───────────────────────────
        frm_turno = ttk.LabelFrame(self, text="Turno actual", padding=10)
        frm_turno.pack(fill="x", pady=(0, 10))

        self._lbl_turno = ttk.Label(
            frm_turno, text="—", font=("Segoe UI", 16, "bold"), foreground="#1565c0"
        )
        self._lbl_turno.pack(side="left", padx=10)

        ttk.Button(frm_turno, text="▶  Siguiente turno",
                   command=self._siguiente_turno).pack(side="left", padx=8)

        # ── Lista de repartidores ──────────────────
        frm_lista = ttk.LabelFrame(self, text="Repartidores registrados", padding=8)
        frm_lista.pack(fill="both", expand=True, pady=(0, 10))

        self._listbox = tk.Listbox(frm_lista, height=10,
                                   font=("Segoe UI", 11), selectmode="browse")
        sc = ttk.Scrollbar(frm_lista, orient="vertical", command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=sc.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        # ── Alta / baja ────────────────────────────
        frm_abm = ttk.LabelFrame(self, text="Alta / Baja", padding=8)
        frm_abm.pack(fill="x")

        frm_agregar = ttk.Frame(frm_abm)
        frm_agregar.pack(fill="x", pady=(0, 4))
        ttk.Label(frm_agregar, text="Nombre:").pack(side="left", padx=(0, 6))
        self._var_nombre = tk.StringVar()
        ttk.Entry(frm_agregar, textvariable=self._var_nombre, width=20).pack(side="left", padx=(0, 6))
        ttk.Button(frm_agregar, text="+ Agregar repartidor",
                   command=self._agregar).pack(side="left")

        frm_quitar = ttk.Frame(frm_abm)
        frm_quitar.pack(fill="x")
        ttk.Label(frm_quitar, text="Nombre:").pack(side="left", padx=(0, 6))
        self._var_quitar = tk.StringVar()
        ttk.Entry(frm_quitar, textvariable=self._var_quitar, width=20).pack(side="left", padx=(0, 6))
        ttk.Button(frm_quitar, text="– Quitar repartidor",
                   command=self._quitar).pack(side="left")

    # ─────────────────────────────────────────────
    # Lógica
    # ─────────────────────────────────────────────

    def _refrescar(self):
        self._listbox.delete(0, "end")
        reps = self.lista.recorrer()
        actual = self.lista.actual()
        for r in reps:
            marca = "  ← turno actual" if r == actual else ""
            self._listbox.insert("end", f"  {r}{marca}")
        self._lbl_turno.config(text=actual if actual else "Sin repartidores")

    def _siguiente_turno(self):
        if self.lista.esta_vacia():
            messagebox.showinfo("Info", "No hay repartidores registrados.")
            return
        self.lista.siguiente_turno()
        self._refrescar()

    def _agregar(self):
        nombre = self._var_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Escribí el nombre del repartidor.")
            return
        # Verificar duplicados
        if nombre in self.lista.recorrer():
            messagebox.showerror("Error", f"'{nombre}' ya está en la lista.")
            return
        self.lista.insertar(nombre)
        self._var_nombre.set("")
        self._refrescar()

    def _quitar(self):
        nombre = self._var_quitar.get().strip()
        if not nombre:
            messagebox.showerror("Error", "Escribí el nombre a quitar.")
            return
        eliminado = self.lista.eliminar(nombre)
        if eliminado:
            self._var_quitar.set("")
            self._refrescar()
        else:
            messagebox.showerror("Error", f"No se encontró '{nombre}' en la lista.")
