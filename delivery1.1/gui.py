"""Interfaz gráfica para el sistema de pedidos usando Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from local import Local, ErrorDeNegocio
from modelos import Producto
from complejidades import info_estructura, listar_todas


class PedidosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pedidos - Local de Comidas")
        self.root.geometry("1400x800")
        self.local = Local()
        
        # Contador de despachados (para estadística correcta)
        self.total_despachados = 0
        
        # Estilos
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.actualizar_todo()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # COLUMNA IZQUIERDA - Pedidos y control
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # --- Crear nuevo pedido ---
        ttk.Label(left_frame, text="NUEVO PEDIDO", font=("Arial", 11, "bold")).pack()
        form_frame = ttk.LabelFrame(left_frame, text="Armado", padding=5)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Cliente
        ttk.Label(form_frame, text="Cliente:").pack(anchor=tk.W)
        self.cliente_entry = ttk.Entry(form_frame, width=30)
        self.cliente_entry.pack(anchor=tk.W, fill=tk.X)
        
        # Zona
        ttk.Label(form_frame, text="Zona (Enter si retira):").pack(anchor=tk.W, pady=(5, 0))
        self.zona_entry = ttk.Entry(form_frame, width=30)
        self.zona_entry.pack(anchor=tk.W, fill=tk.X)
        
        # Producto
        ttk.Label(form_frame, text="Código producto:").pack(anchor=tk.W, pady=(5, 0))
        prod_frame = ttk.Frame(form_frame)
        prod_frame.pack(fill=tk.X, pady=5)
        self.codigo_entry = ttk.Entry(prod_frame, width=10)
        self.codigo_entry.pack(side=tk.LEFT, padx=2)
        self.cantidad_var = tk.IntVar(value=1)
        self.cantidad_spin = ttk.Spinbox(prod_frame, from_=1, to=99, textvariable=self.cantidad_var, width=5)
        self.cantidad_spin.pack(side=tk.LEFT, padx=2)
        ttk.Button(prod_frame, text="Agregar", command=self.agregar_producto).pack(side=tk.LEFT, padx=2)
        ttk.Button(prod_frame, text="Quitar último", command=self.quitar_ultimo_producto).pack(side=tk.LEFT, padx=2)
        
        # Urgencia
        self.urgente_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="¿Es urgente?", variable=self.urgente_var, 
                        command=self.toggle_urgencia).pack(anchor=tk.W, pady=5)
        
        # Minutos (solo si es urgente)
        ttk.Label(form_frame, text="Minutos promesa:").pack(anchor=tk.W)
        self.minutos_entry = ttk.Entry(form_frame, width=10)
        self.minutos_entry.insert(0, "15")
        self.minutos_entry.pack(anchor=tk.W)
        
        # Botones confirmar/cancelar
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="✓ Confirmar", command=self.confirmar_pedido).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="✗ Cancelar", command=self.cancelar_pedido).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📊 Cargar Demo", command=self.cargar_demo).pack(side=tk.LEFT, padx=2)
        
        # --- Productos cargados ---
        ttk.Label(left_frame, text="PRODUCTOS DEL PEDIDO", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.items_listbox = tk.Listbox(left_frame, height=5, font=("Courier", 9))
        self.items_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Total
        self.total_label = ttk.Label(left_frame, text="TOTAL: $0", font=("Arial", 10, "bold"))
        self.total_label.pack(pady=5)
        
        # --- Pedidos en espera ---
        ttk.Label(left_frame, text="PEDIDOS EN ESPERA", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        self.pedidos_listbox = tk.Listbox(left_frame, height=8, font=("Courier", 8))
        self.pedidos_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botones despacho
        btn_frame2 = ttk.Frame(left_frame)
        btn_frame2.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame2, text="Despachar siguiente", command=self.despachar_pedido).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="Refrescar", command=self.actualizar_todo).pack(side=tk.LEFT, padx=2)
        
        # --- Despachados ---
        ttk.Label(left_frame, text="ÚLTIMOS DESPACHADOS", font=("Arial", 10, "bold")).pack()
        self.despachados_listbox = tk.Listbox(left_frame, height=3, font=("Courier", 8))
        self.despachados_listbox.pack(fill=tk.X, pady=5)
        
        # COLUMNA DERECHA - Información
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña: Catálogo
        cat_frame = ttk.Frame(notebook)
        notebook.add(cat_frame, text="Catálogo")
        ttk.Label(cat_frame, text="PRODUCTOS (por código)", font=("Arial", 10, "bold")).pack()
        self.catalogo_listbox = tk.Listbox(cat_frame, font=("Courier", 8))
        self.catalogo_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Pestaña: Búsquedas
        search_frame = ttk.Frame(notebook)
        notebook.add(search_frame, text="Búsquedas")
        ttk.Label(search_frame, text="BUSCAR", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Búsqueda por precio exacto (binaria)
        ttk.Label(search_frame, text="Producto por precio exacto:").pack(anchor=tk.W, padx=5)
        precio_frame = ttk.Frame(search_frame)
        precio_frame.pack(fill=tk.X, padx=5)
        self.precio_entry = ttk.Entry(precio_frame, width=15)
        self.precio_entry.pack(side=tk.LEFT, padx=2)
        ttk.Button(precio_frame, text="Buscar", command=self.buscar_por_precio).pack(side=tk.LEFT, padx=2)
        self.precio_result = ttk.Label(search_frame, text="", foreground="blue")
        self.precio_result.pack(anchor=tk.W, padx=5, pady=5)
        
        # Búsqueda por nombre (secuencial)
        ttk.Label(search_frame, text="Producto por nombre:").pack(anchor=tk.W, padx=5, pady=(10, 0))
        nombre_frame = ttk.Frame(search_frame)
        nombre_frame.pack(fill=tk.X, padx=5)
        self.nombre_entry = ttk.Entry(nombre_frame, width=15)
        self.nombre_entry.pack(side=tk.LEFT, padx=2)
        ttk.Button(nombre_frame, text="Buscar", command=self.buscar_por_nombre).pack(side=tk.LEFT, padx=2)
        self.nombre_result = ttk.Label(search_frame, text="", foreground="blue")
        self.nombre_result.pack(anchor=tk.W, padx=5, pady=5)
        
        # Combo por presupuesto (backtracking)
        ttk.Label(search_frame, text="Combo por presupuesto:").pack(anchor=tk.W, padx=5, pady=(10, 0))
        combo_frame = ttk.Frame(search_frame)
        combo_frame.pack(fill=tk.X, padx=5)
        self.presupuesto_entry = ttk.Entry(combo_frame, width=15)
        self.presupuesto_entry.pack(side=tk.LEFT, padx=2)
        ttk.Button(combo_frame, text="Buscar", command=self.buscar_combo).pack(side=tk.LEFT, padx=2)
        self.combo_result = ttk.Label(search_frame, text="", foreground="blue")
        self.combo_result.pack(anchor=tk.W, padx=5, pady=5)
        
        # Pestaña: Calculadora
        calc_frame = ttk.Frame(notebook)
        notebook.add(calc_frame, text="Calculadora")
        ttk.Label(calc_frame, text="Evaluar cuenta (postfija)", font=("Arial", 10, "bold")).pack(pady=5)
        ttk.Label(calc_frame, text="Ejemplo: (5500 + 3000) * 90 / 100").pack(anchor=tk.W, padx=5)
        self.cuenta_entry = ttk.Entry(calc_frame, width=30)
        self.cuenta_entry.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(calc_frame, text="Calcular", command=self.calcular).pack(pady=5)
        self.cuenta_result = ttk.Label(calc_frame, text="", font=("Arial", 12, "bold"), foreground="green")
        self.cuenta_result.pack(pady=10)
        
        # Pestaña: Zonas
        zone_frame = ttk.Frame(notebook)
        notebook.add(zone_frame, text="Zonas")
        ttk.Label(zone_frame, text="ZONAS DE ENTREGA", font=("Arial", 10, "bold")).pack()
        self.zonas_text = tk.Text(zone_frame, height=12, font=("Courier", 8))
        self.zonas_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Pestaña: Estadísticas
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Estadísticas")
        self.stats_text = tk.Text(stats_frame, height=12, font=("Courier", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Pestaña: Estructuras
        struct_frame = ttk.Frame(notebook)
        notebook.add(struct_frame, text="Estructuras")
        
        select_frame = ttk.Frame(struct_frame)
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(select_frame, text="Ver complejidad de:").pack(side=tk.LEFT, padx=5)
        self.estructura_var = tk.StringVar()
        self.estructura_combo = ttk.Combobox(
            select_frame,
            textvariable=self.estructura_var,
            values=listar_todas(),
            state="readonly",
            width=30
        )
        self.estructura_combo.pack(side=tk.LEFT, padx=5)
        self.estructura_combo.bind("<<ComboboxSelected>>", lambda e: self.actualizar_estructura())
        
        if listar_todas():
            self.estructura_combo.current(0)
        
        self.estructura_text = tk.Text(struct_frame, height=12, font=("Courier", 8))
        self.estructura_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def formato_precio(self, precio):
        """Formatea el precio como moneda."""
        return "$" + f"{precio:,.0f}".replace(",", ".")
    
    def toggle_urgencia(self):
        """Habilita/deshabilita entrada de minutos según urgencia."""
        self.minutos_entry.config(state=tk.NORMAL if self.urgente_var.get() else tk.DISABLED)
    
    def actualizar_todo(self):
        """Actualiza toda la interfaz."""
        self.actualizar_pedidos()
        self.actualizar_items()
        self.actualizar_catalogo()
        self.actualizar_zonas()
        self.actualizar_estadisticas()
        self.actualizar_despachados()
        self.actualizar_estructura()
    
    def actualizar_items(self):
        """Actualiza la lista de productos del pedido en armado."""
        self.items_listbox.delete(0, tk.END)
        
        if self.local.pedido_actual is None:
            self.items_listbox.insert(tk.END, "(Sin pedido en armado)")
            self.total_label.config(text="TOTAL: $0")
            return
        
        pedido = self.local.pedido_actual
        items = list(pedido.items)
        
        if not items:
            self.items_listbox.insert(tk.END, "(Sin productos)")
        else:
            for item in items:
                linea = f"{item.codigo}  {item.nombre:<20}  {self.formato_precio(item.precio)}"
                self.items_listbox.insert(tk.END, linea)
        
        total = pedido.total()
        self.total_label.config(text=f"TOTAL: {self.formato_precio(total)}")
    
    def agregar_producto(self):
        """Agrega un producto al pedido en armado."""
        if self.local.pedido_actual is None:
            # Iniciar pedido automáticamente
            cliente = self.cliente_entry.get().strip()
            if not cliente:
                messagebox.showerror("Error", "Ingresá el nombre del cliente")
                return
            
            zona = self.zona_entry.get().strip() or ""
            
            try:
                self.local.iniciar_pedido(cliente, zona)
            except ErrorDeNegocio as e:
                messagebox.showerror("Error", str(e))
                return
        
        try:
            codigo = int(self.codigo_entry.get())
            cantidad = self.cantidad_var.get()
            
            for _ in range(cantidad):
                self.local.agregar(codigo)
            
            self.codigo_entry.delete(0, tk.END)
            self.cantidad_var.set(1)
            self.actualizar_items()
            
        except ValueError:
            messagebox.showerror("Error", "Ingresá un código válido")
        except ErrorDeNegocio as e:
            messagebox.showerror("Error", str(e))
    
    def quitar_ultimo_producto(self):
        """Quita el último producto del pedido."""
        try:
            self.local.quitar_ultimo()
            self.actualizar_items()
        except ErrorDeNegocio as e:
            messagebox.showerror("Error", str(e))
    
    def confirmar_pedido(self):
        """Confirma el pedido en armado."""
        try:
            urgente = self.urgente_var.get()
            minutos = 15
            
            if urgente:
                try:
                    minutos = int(self.minutos_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Ingresá minutos válidos")
                    return
            
            pedido = self.local.confirmar(urgente, minutos)
            
            messagebox.showinfo("Éxito", 
                f"Pedido #{pedido.id} de {pedido.cliente} confirmado\n"
                f"Total: {self.formato_precio(pedido.total())}")
            
            # Limpiar formulario
            self.cliente_entry.delete(0, tk.END)
            self.zona_entry.delete(0, tk.END)
            self.urgente_var.set(False)
            self.toggle_urgencia()
            
            self.actualizar_todo()
            
        except ErrorDeNegocio as e:
            messagebox.showerror("Error al confirmar", str(e))
            # ARREGLO: Cancelar pedido si confirmar falla
            try:
                self.local.cancelar()
            except:
                pass
            self.actualizar_todo()
    
    def cancelar_pedido(self):
        """Cancela el pedido en armado."""
        try:
            self.local.cancelar()
            messagebox.showinfo("Cancelado", "Pedido cancelado")
            
            # Limpiar formulario
            self.cliente_entry.delete(0, tk.END)
            self.zona_entry.delete(0, tk.END)
            self.urgente_var.set(False)
            self.toggle_urgencia()
            
            self.actualizar_todo()
        except ErrorDeNegocio as e:
            messagebox.showerror("Error", str(e))
    
    def actualizar_pedidos(self):
        """Actualiza la lista de pedidos en espera."""
        self.pedidos_listbox.delete(0, tk.END)
        espera = self.local.en_espera()
        
        if not espera:
            self.pedidos_listbox.insert(tk.END, "No hay pedidos en espera")
            return
        
        for i, p in enumerate(espera, 1):
            urgente_str = "[URGENTE]" if p.urgente else ""
            items_count = len(list(p.items))
            linea = f"{i}. #{p.id:3} {p.cliente:15} {p.zona:12} {self.formato_precio(p.total()):8} {urgente_str}"
            self.pedidos_listbox.insert(tk.END, linea)
    
    def despachar_pedido(self):
        """Despacha el siguiente pedido."""
        try:
            p = self.local.despachar()
            self.total_despachados += 1
            quien = f"con {p.repartidor}" if p.repartidor else "(retira en el local)"
            messagebox.showinfo("Despachado", 
                f"Pedido #{p.id} de {p.cliente}\n{quien}")
            self.actualizar_todo()
        except ErrorDeNegocio as e:
            messagebox.showerror("Error", str(e))
    
    def actualizar_catalogo(self):
        """Actualiza el catálogo de productos."""
        self.catalogo_listbox.delete(0, tk.END)
        for p in self.local.productos_por_codigo():
            linea = f"{p.codigo}  {p.nombre:<20}  {self.formato_precio(p.precio):>8}"
            self.catalogo_listbox.insert(tk.END, linea)
    
    def buscar_por_precio(self):
        """Busca un producto por precio exacto (búsqueda binaria)."""
        try:
            precio = int(self.precio_entry.get())
            p = self.local.buscar_por_precio(precio)
            if p:
                self.precio_result.config(text=f"✓ {p.codigo} - {p.nombre} (${p.precio})")
            else:
                self.precio_result.config(text="✗ No encontrado")
        except ValueError:
            self.precio_result.config(text="✗ Ingresá un precio válido")
    
    def buscar_por_nombre(self):
        """Busca un producto por nombre (búsqueda secuencial)."""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            self.nombre_result.config(text="✗ Ingresá un nombre")
            return
        
        p = self.local.buscar_por_nombre(nombre)
        if p:
            self.nombre_result.config(text=f"✓ {p.codigo} - {p.nombre} ({self.formato_precio(p.precio)})")
        else:
            self.nombre_result.config(text="✗ No encontrado")
    
    def buscar_combo(self):
        """Busca un combo que sume el presupuesto (backtracking)."""
        try:
            presupuesto = int(self.presupuesto_entry.get())
            combo = self.local.combo(presupuesto)
            if combo:
                nombres = ", ".join(p.nombre for p in combo)
                total = sum(p.precio for p in combo)
                self.combo_result.config(text=f"✓ {nombres} = {self.formato_precio(total)}")
            else:
                self.combo_result.config(text="✗ Sin combinación exacta")
        except ValueError:
            self.combo_result.config(text="✗ Ingresá un presupuesto válido")
    
    def calcular(self):
        """Calcula una expresión con postfija."""
        cuenta = self.cuenta_entry.get().strip()
        if not cuenta:
            self.cuenta_result.config(text="")
            return
        
        try:
            resultado = self.local.calcular(cuenta)
            self.cuenta_result.config(text=self.formato_precio(resultado))
        except ErrorDeNegocio as e:
            self.cuenta_result.config(text=f"Error: {e}", foreground="red")
    
    def actualizar_zonas(self):
        """Actualiza información de zonas."""
        self.zonas_text.delete(1.0, tk.END)
        
        zonas_alcanzables = self.local.zonas_alcanzables()
        self.zonas_text.insert(tk.END, "Zonas alcanzables:\n")
        self.zonas_text.insert(tk.END, ", ".join(zonas_alcanzables) + "\n\n")
        
        self.zonas_text.insert(tk.END, "Recorrido BFS:\n")
        self.zonas_text.insert(tk.END, " -> ".join(self.local.recorrido_por_anchura()) + "\n\n")
        
        self.zonas_text.insert(tk.END, "Rutas más cortas:\n")
        for zona in zonas_alcanzables:
            ruta = self.local.ruta(zona)
            if ruta:
                self.zonas_text.insert(tk.END, f"  {zona}: {' -> '.join(ruta)}\n")
    
    def actualizar_estadisticas(self):
        """Actualiza estadísticas del sistema."""
        self.stats_text.delete(1.0, tk.END)
        
        espera = self.local.en_espera()
        total_espera = sum(p.total() for p in espera)
        
        self.stats_text.insert(tk.END, "ESTADÍSTICAS DEL SISTEMA\n")
        self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
        self.stats_text.insert(tk.END, f"Pedidos en espera: {len(espera)}\n")
        self.stats_text.insert(tk.END, f"Dinero en espera: {self.formato_precio(total_espera)}\n")
        self.stats_text.insert(tk.END, f"Total pedidos despachados: {self.total_despachados}\n")
        self.stats_text.insert(tk.END, f"En pizarra (últimos 3): {len(self.local.listos)}\n\n")
        
        self.stats_text.insert(tk.END, "Catálogo:\n")
        productos = list(self.local.productos_por_codigo())
        self.stats_text.insert(tk.END, f"  Total de productos: {len(productos)}\n")
        
        productos_por_precio = list(self.local.productos_por_precio())
        if productos_por_precio:
            self.stats_text.insert(tk.END, f"  Más caro: {productos_por_precio[-1].nombre} ({self.formato_precio(productos_por_precio[-1].precio)})\n")
            self.stats_text.insert(tk.END, f"  Más barato: {productos_por_precio[0].nombre} ({self.formato_precio(productos_por_precio[0].precio)})\n")
        
        self.stats_text.insert(tk.END, f"\nÁrbol AVL del catálogo:\n")
        if hasattr(self.local, 'catalogo'):
            self.stats_text.insert(tk.END, f"  Altura: {self.local.catalogo.altura()}\n")
            self.stats_text.insert(tk.END, f"  Nodos: {len(self.local.catalogo)}\n")
        
        self.stats_text.insert(tk.END, f"\nRepartidores disponibles: {len(list(self.local.repartidores))}\n")
    
    def actualizar_despachados(self):
        """Actualiza el historial de despachados."""
        self.despachados_listbox.delete(0, tk.END)
        if not self.local.listos:
            self.despachados_listbox.insert(tk.END, "Sin pedidos despachados")
            return
        
        for p in self.local.listos:
            linea = f"#{p.id} {p.cliente:<15} {self.formato_precio(p.total()):>8}  ({p.repartidor or 'Retira'})"
            self.despachados_listbox.insert(tk.END, linea)
    
    def actualizar_estructura(self):
        """Actualiza la información de la estructura seleccionada."""
        estructura_nombre = self.estructura_var.get()
        info = info_estructura(estructura_nombre)
        
        self.estructura_text.delete(1.0, tk.END)
        
        if not info:
            self.estructura_text.insert(tk.END, "Estructura no encontrada")
            return
        
        # Encabezado
        self.estructura_text.insert(tk.END, f"{'='*60}\n")
        self.estructura_text.insert(tk.END, f"{estructura_nombre}\n")
        self.estructura_text.insert(tk.END, f"{'='*60}\n\n")
        
        # Descripción
        self.estructura_text.insert(tk.END, f"Descripción:\n{info['descripcion']}\n\n")
        
        # Operaciones principales
        self.estructura_text.insert(tk.END, f"Operaciones principales:\n{info['operacion']}\n\n")
        
        # Complejidad
        self.estructura_text.insert(tk.END, "COMPLEJIDAD ASINTÓTICA:\n")
        self.estructura_text.insert(tk.END, f"  Big O (peor caso):     {info['big_o']}\n")
        self.estructura_text.insert(tk.END, f"  Theta (promedio):      {info['theta']}\n")
        self.estructura_text.insert(tk.END, f"  Omega (mejor caso):    {info['omega']}\n\n")
        
        # Usos en el local
        self.estructura_text.insert(tk.END, f"Usos en este local:\n")
        for uso in info['usos']:
            self.estructura_text.insert(tk.END, f"  • {uso}\n")
    
    def cargar_demo(self):
        """Carga datos de demostración."""
        try:
            # 1. Pedido de Ana (con quitar último - pila)
            self.local.iniciar_pedido("Ana", "Norte")
            for codigo in (101, 103, 104, 104):
                self.local.agregar(codigo)
            self.local.quitar_ultimo()  # Demuestra pila
            self.local.confirmar()
            
            # 2. Pedidos: normal, urgente x2
            self.local.iniciar_pedido("Beto", "")
            self.local.agregar(105)
            self.local.confirmar(False)
            
            self.local.iniciar_pedido("Cami", "Sur")
            self.local.agregar(102)
            self.local.confirmar(True, 20)  # Cola de prioridad
            
            self.local.iniciar_pedido("Dani", "Costanera")
            self.local.agregar(107)
            self.local.confirmar(True, 10)
            
            # 3. Despachar todos
            for _ in range(4):
                self.local.despachar()
                self.total_despachados += 1
            
            self.actualizar_todo()
            messagebox.showinfo("Demo", "Datos de demostración cargados")
            
        except ErrorDeNegocio as e:
            messagebox.showerror("Error en demo", str(e))


def main():
    root = tk.Tk()
    app = PedidosGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
