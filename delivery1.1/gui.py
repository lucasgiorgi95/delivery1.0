"""Interfaz gráfica OPTIMIZADA - Sistema de Pedidos usando Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
from local import Local, ErrorDeNegocio
from complejidades import info_estructura, listar_todas


class PedidosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pedidos - Local de Comidas")
        self.root.geometry("1500x850")
        self.local = Local()
        
        self.total_despachados = 0
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cache de datos
        self.zonas_list = ["Retira en el local"] + list(self.local.zonas_alcanzables())
        self.productos_list = list(self.local.productos_por_codigo())
        
        self.setup_ui()
        self.actualizar_todo()
    
    def setup_ui(self):
        """Interfaz completamente optimizada con selecciones."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # COLUMNA IZQUIERDA
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # === SECCIÓN 1: CREAR PEDIDO ===
        ttk.Label(left_frame, text="➕ CREAR PEDIDO", font=("Arial", 13, "bold")).pack(pady=(0, 5))
        form_frame = ttk.LabelFrame(left_frame, text="Nuevo Pedido", padding=10)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Cliente
        ttk.Label(form_frame, text="Nombre del cliente:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.cliente_entry = ttk.Entry(form_frame, width=40, font=("Arial", 10))
        self.cliente_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 8))
        
        # Zona - COMBOBOX
        ttk.Label(form_frame, text="Zona de entrega:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.zona_var = tk.StringVar(value=self.zonas_list[0])
        zona_combo = ttk.Combobox(form_frame, textvariable=self.zona_var, 
                                   values=self.zonas_list, state="readonly", font=("Arial", 10))
        zona_combo.pack(anchor=tk.W, fill=tk.X, pady=(0, 8))
        
        # Producto - COMBOBOX
        ttk.Label(form_frame, text="Seleccionar producto:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.producto_var = tk.StringVar()
        self.prod_combo = ttk.Combobox(form_frame, textvariable=self.producto_var, state="readonly", font=("Arial", 10))
        self.prod_combo.pack(anchor=tk.W, fill=tk.X, pady=(0, 8))
        self._actualizar_combo_productos()
        
        # Cantidad
        qty_lbl_frame = ttk.Frame(form_frame)
        qty_lbl_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(qty_lbl_frame, text="Cantidad:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.cantidad_var = tk.IntVar(value=1)
        ttk.Spinbox(qty_lbl_frame, from_=1, to=99, textvariable=self.cantidad_var, width=5, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(btn_frame, text="➕ AGREGAR", command=self.agregar_producto).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_frame, text="🗑️ QUITAR", command=self.quitar_ultimo_producto).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Urgencia
        self.urgente_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="🔴 Es URGENTE", variable=self.urgente_var, command=self.toggle_urgencia).pack(anchor=tk.W, pady=(0, 8))
        
        # Minutos
        min_frame = ttk.Frame(form_frame)
        min_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(min_frame, text="Minutos promesa:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.minutos_var = tk.IntVar(value=15)
        self.minutos_spin = ttk.Spinbox(min_frame, from_=5, to=120, textvariable=self.minutos_var, width=5, font=("Arial", 10))
        self.minutos_spin.pack(side=tk.LEFT)
        self.minutos_spin.config(state=tk.DISABLED)
        
        # Confirmar/Cancelar
        btn_conf_frame = ttk.Frame(form_frame)
        btn_conf_frame.pack(fill=tk.X)
        ttk.Button(btn_conf_frame, text="✅ CONFIRMAR", command=self.confirmar_pedido).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(btn_conf_frame, text="❌ CANCELAR", command=self.cancelar_pedido).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # === SECCIÓN 2: PRODUCTOS CARGADOS ===
        ttk.Label(left_frame, text="📦 PRODUCTOS CARGADOS", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        self.items_listbox = tk.Listbox(left_frame, height=6, font=("Courier", 9))
        self.items_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.total_label = ttk.Label(left_frame, text="TOTAL: $0", font=("Arial", 11, "bold"), foreground="darkgreen")
        self.total_label.pack(pady=5)
        
        # === SECCIÓN 3: PEDIDOS EN ESPERA ===
        ttk.Label(left_frame, text="📋 PEDIDOS EN ESPERA", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        self.pedidos_listbox = tk.Listbox(left_frame, height=8, font=("Courier", 8))
        self.pedidos_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botones despacho
        btn_desp = ttk.Frame(left_frame)
        btn_desp.pack(fill=tk.X, pady=5)
        ttk.Button(btn_desp, text="📦 DESPACHAR", command=self.despachar_pedido).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(btn_desp, text="🔄 REFRESCAR", command=self.actualizar_todo).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(btn_desp, text="📊 DEMO", command=self.cargar_demo).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        # === SECCIÓN 4: ÚLTIMOS DESPACHADOS ===
        ttk.Label(left_frame, text="✅ ÚLTIMOS DESPACHADOS", font=("Arial", 10, "bold")).pack(pady=(5, 0))
        self.despachados_listbox = tk.Listbox(left_frame, height=3, font=("Courier", 8))
        self.despachados_listbox.pack(fill=tk.X, pady=5)
        
        # COLUMNA DERECHA - PESTAÑAS
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self._setup_catalogo_tab()
        self._setup_busquedas_tab()
        self._setup_calculadora_tab()
        self._setup_zonas_tab()
        self._setup_estadisticas_tab()
        self._setup_estructuras_tab()
    
    def _setup_catalogo_tab(self):
        cat_frame = ttk.Frame(self.notebook)
        self.notebook.add(cat_frame, text="📋 Catálogo")
        ttk.Label(cat_frame, text="Todos los productos (ordenados por código)").pack(pady=5, padx=5)
        self.catalogo_listbox = tk.Listbox(cat_frame, font=("Courier", 9))
        self.catalogo_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _setup_busquedas_tab(self):
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="🔍 Búsquedas")
        
        # Por precio
        ttk.Label(search_frame, text="🔍 Por PRECIO EXACTO (búsqueda binaria):", font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=5, pady=(5, 0))
        precios = sorted(set(p.precio for p in self.productos_list))
        precio_frame = ttk.Frame(search_frame)
        precio_frame.pack(fill=tk.X, padx=5, pady=5)
        self.precio_combo = ttk.Combobox(precio_frame, values=precios, state="readonly", width=15, font=("Arial", 10))
        self.precio_combo.pack(side=tk.LEFT, padx=2)
        ttk.Button(precio_frame, text="Buscar", command=self.buscar_por_precio).pack(side=tk.LEFT, padx=2)
        self.precio_result = ttk.Label(search_frame, text="", foreground="blue", font=("Arial", 9))
        self.precio_result.pack(anchor=tk.W, padx=5, pady=5)
        
        # Por nombre
        ttk.Label(search_frame, text="🔍 Por NOMBRE (búsqueda secuencial):", font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=5, pady=(10, 0))
        nombres = [p.nombre for p in self.productos_list]
        nombre_frame = ttk.Frame(search_frame)
        nombre_frame.pack(fill=tk.X, padx=5, pady=5)
        self.nombre_combo = ttk.Combobox(nombre_frame, values=nombres, state="readonly", font=("Arial", 10))
        self.nombre_combo.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(nombre_frame, text="Buscar", command=self.buscar_por_nombre).pack(side=tk.LEFT, padx=2)
        self.nombre_result = ttk.Label(search_frame, text="", foreground="blue", font=("Arial", 9))
        self.nombre_result.pack(anchor=tk.W, padx=5, pady=5)
        
        # Combo
        ttk.Label(search_frame, text="🎯 COMBO por PRESUPUESTO (backtracking):", font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=5, pady=(10, 0))
        combo_frame = ttk.Frame(search_frame)
        combo_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(combo_frame, text="Presupuesto ($):").pack(side=tk.LEFT, padx=2)
        self.presupuesto_spin = ttk.Spinbox(combo_frame, from_=100, to=50000, increment=100, width=10, font=("Arial", 10))
        self.presupuesto_spin.set(10000)
        self.presupuesto_spin.pack(side=tk.LEFT, padx=2)
        ttk.Button(combo_frame, text="Buscar", command=self.buscar_combo).pack(side=tk.LEFT, padx=2)
        self.combo_result = ttk.Label(search_frame, text="", foreground="blue", wraplength=400, font=("Arial", 9), justify=tk.LEFT)
        self.combo_result.pack(anchor=tk.W, padx=5, pady=5)
    
    def _setup_calculadora_tab(self):
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="🧮 Calculadora")
        ttk.Label(calc_frame, text="Evaluar Expresión (notación postfija)", font=("Arial", 10, "bold")).pack(pady=5)
        ttk.Label(calc_frame, text="Expresión:").pack(anchor=tk.W, padx=5)
        self.cuenta_entry = ttk.Entry(calc_frame, width=40, font=("Arial", 10))
        self.cuenta_entry.pack(fill=tk.X, padx=5, pady=5)
        self.cuenta_entry.insert(0, "(5500 + 3000) * 90 / 100")
        ttk.Button(calc_frame, text="Calcular", command=self.calcular).pack(pady=5)
        self.cuenta_result = ttk.Label(calc_frame, text="", font=("Arial", 20, "bold"), foreground="green")
        self.cuenta_result.pack(pady=10)
    
    def _setup_zonas_tab(self):
        zone_frame = ttk.Frame(self.notebook)
        self.notebook.add(zone_frame, text="🗺️ Zonas")
        ttk.Label(zone_frame, text="Mapa de Rutas").pack(pady=5, padx=5)
        self.zonas_text = tk.Text(zone_frame, height=20, font=("Courier", 9))
        self.zonas_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _setup_estadisticas_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📈 Estadísticas")
        self.stats_text = tk.Text(stats_frame, height=20, font=("Courier", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _setup_estructuras_tab(self):
        struct_frame = ttk.Frame(self.notebook)
        self.notebook.add(struct_frame, text="⚙️ Estructuras")
        
        select_frame = ttk.Frame(struct_frame)
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(select_frame, text="Ver estructura:").pack(side=tk.LEFT, padx=5)
        self.estructura_var = tk.StringVar()
        self.estructura_combo = ttk.Combobox(select_frame, textvariable=self.estructura_var,
                                             values=listar_todas(), state="readonly", width=30)
        self.estructura_combo.pack(side=tk.LEFT, padx=5)
        self.estructura_combo.bind("<<ComboboxSelected>>", lambda e: self.actualizar_estructura())
        
        if listar_todas():
            self.estructura_combo.current(0)
        
        self.estructura_text = tk.Text(struct_frame, height=20, font=("Courier", 8))
        self.estructura_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _actualizar_combo_productos(self):
        """Actualiza combo de productos."""
        productos_display = [f"{p.codigo} - {p.nombre} (${p.precio})" for p in self.productos_list]
        self.prod_combo['values'] = productos_display
        if productos_display:
            self.prod_combo.current(0)
    
    def formato_precio(self, precio):
        return "$" + f"{precio:,.0f}".replace(",", ".")
    
    def toggle_urgencia(self):
        state = tk.NORMAL if self.urgente_var.get() else tk.DISABLED
        self.minutos_spin.config(state=state)
    
    def actualizar_todo(self):
        self.actualizar_items()
        self.actualizar_pedidos()
        self.actualizar_catalogo()
        self.actualizar_zonas()
        self.actualizar_estadisticas()
        self.actualizar_despachados()
        self.actualizar_estructura()
    
    def actualizar_items(self):
        self.items_listbox.delete(0, tk.END)
        
        if self.local.pedido_actual is None:
            self.items_listbox.insert(tk.END, "(Sin pedido)")
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
        
        self.total_label.config(text=f"TOTAL: {self.formato_precio(pedido.total())}")
    
    def agregar_producto(self):
        if self.local.pedido_actual is None:
            cliente = self.cliente_entry.get().strip()
            if not cliente:
                messagebox.showerror("Error", "Ingresá el nombre del cliente")
                return
            
            zona = self.zona_var.get()
            try:
                self.local.iniciar_pedido(cliente, zona)
            except ErrorDeNegocio as e:
                messagebox.showerror("Error", str(e))
                return
        
        try:
            prod_text = self.producto_var.get()
            codigo = int(prod_text.split(" ")[0])
            cantidad = self.cantidad_var.get()
            
            for _ in range(cantidad):
                self.local.agregar(codigo)
            
            self.cantidad_var.set(1)
            self.actualizar_items()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def quitar_ultimo_producto(self):
        try:
            self.local.quitar_ultimo()
            self.actualizar_items()
        except ErrorDeNegocio as e:
            messagebox.showerror("Error", str(e))
    
    def confirmar_pedido(self):
        try:
            urgente = self.urgente_var.get()
            minutos = self.minutos_var.get() if urgente else 15
            
            pedido = self.local.confirmar(urgente, minutos)
            
            messagebox.showinfo("✅ Éxito", 
                f"Pedido #{pedido.id} de {pedido.cliente}\nTotal: {self.formato_precio(pedido.total())}")
            
            self.cliente_entry.delete(0, tk.END)
            self.zona_var.set(self.zonas_list[0])
            self.urgente_var.set(False)
            self.toggle_urgencia()
            
            self.actualizar_todo()
            
        except ErrorDeNegocio as e:
            messagebox.showerror("❌ Error", str(e))
            try:
                self.local.cancelar()
            except:
                pass
            self.actualizar_todo()
    
    def cancelar_pedido(self):
        try:
            self.local.cancelar()
            messagebox.showinfo("Cancelado", "Pedido cancelado")
            
            self.cliente_entry.delete(0, tk.END)
            self.zona_var.set(self.zonas_list[0])
            self.urgente_var.set(False)
            self.toggle_urgencia()
            
            self.actualizar_todo()
        except ErrorDeNegocio as e:
            messagebox.showerror("Error", str(e))
    
    def actualizar_pedidos(self):
        self.pedidos_listbox.delete(0, tk.END)
        espera = self.local.en_espera()
        
        if not espera:
            self.pedidos_listbox.insert(tk.END, "✅ No hay pedidos")
            return
        
        for i, p in enumerate(espera, 1):
            urgente_str = "🔴" if p.urgente else "⚪"
            linea = f"{i}. #{p.id:3} {p.cliente:15} {p.zona:12} {self.formato_precio(p.total()):8} {urgente_str}"
            self.pedidos_listbox.insert(tk.END, linea)
    
    def despachar_pedido(self):
        try:
            p = self.local.despachar()
            self.total_despachados += 1
            quien = f"📦 {p.repartidor}" if p.repartidor else "🏠 Retira"
            messagebox.showinfo("✅ Despachado", f"#{p.id} {p.cliente}\n{quien}")
            self.actualizar_todo()
        except ErrorDeNegocio as e:
            messagebox.showerror("❌ Error", str(e))
    
    def actualizar_catalogo(self):
        self.catalogo_listbox.delete(0, tk.END)
        for p in self.local.productos_por_codigo():
            linea = f"{p.codigo}  {p.nombre:<25}  {self.formato_precio(p.precio):>8}"
            self.catalogo_listbox.insert(tk.END, linea)
    
    def buscar_por_precio(self):
        try:
            precio = int(self.precio_combo.get())
            p = self.local.buscar_por_precio(precio)
            if p:
                self.precio_result.config(text=f"✅ {p.codigo} - {p.nombre} (${p.precio})")
            else:
                self.precio_result.config(text="❌ No encontrado")
        except:
            self.precio_result.config(text="❌ Selecciona un precio")
    
    def buscar_por_nombre(self):
        nombre = self.nombre_combo.get()
        if not nombre:
            self.nombre_result.config(text="❌ Selecciona un producto")
            return
        
        p = self.local.buscar_por_nombre(nombre)
        if p:
            self.nombre_result.config(text=f"✅ {p.codigo} - {p.nombre} ({self.formato_precio(p.precio)})")
        else:
            self.nombre_result.config(text="❌ No encontrado")
    
    def buscar_combo(self):
        try:
            presupuesto = int(self.presupuesto_spin.get())
            combo = self.local.combo(presupuesto)
            if combo:
                nombres = " + ".join(p.nombre for p in combo)
                total = sum(p.precio for p in combo)
                self.combo_result.config(text=f"✅ {nombres}\n= {self.formato_precio(total)}")
            else:
                self.combo_result.config(text="❌ Sin combinación exacta")
        except:
            self.combo_result.config(text="❌ Error")
    
    def calcular(self):
        cuenta = self.cuenta_entry.get().strip()
        if not cuenta:
            self.cuenta_result.config(text="")
            return
        
        try:
            resultado = self.local.calcular(cuenta)
            self.cuenta_result.config(text=self.formato_precio(resultado))
        except ErrorDeNegocio as e:
            self.cuenta_result.config(text=f"❌ Error", foreground="red")
    
    def actualizar_zonas(self):
        self.zonas_text.delete(1.0, tk.END)
        
        zonas = self.local.zonas_alcanzables()
        self.zonas_text.insert(tk.END, "📍 Zonas alcanzables:\n")
        self.zonas_text.insert(tk.END, ", ".join(zonas) + "\n\n")
        
        self.zonas_text.insert(tk.END, "📊 Recorrido BFS:\n")
        self.zonas_text.insert(tk.END, " → ".join(self.local.recorrido_por_anchura()) + "\n\n")
        
        self.zonas_text.insert(tk.END, "🛣️ Rutas más cortas:\n")
        for zona in zonas:
            ruta = self.local.ruta(zona)
            if ruta:
                self.zonas_text.insert(tk.END, f"  {zona:15} {' → '.join(ruta)}\n")
    
    def actualizar_estadisticas(self):
        self.stats_text.delete(1.0, tk.END)
        
        espera = self.local.en_espera()
        total_espera = sum(p.total() for p in espera)
        
        self.stats_text.insert(tk.END, "📊 ESTADÍSTICAS\n")
        self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
        self.stats_text.insert(tk.END, f"📦 En espera: {len(espera)}\n")
        self.stats_text.insert(tk.END, f"💵 Dinero en espera: {self.formato_precio(total_espera)}\n")
        self.stats_text.insert(tk.END, f"✅ Total despachados: {self.total_despachados}\n")
        self.stats_text.insert(tk.END, f"📋 En pizarra: {len(self.local.listos)}\n\n")
        
        self.stats_text.insert(tk.END, "📚 Catálogo:\n")
        productos = list(self.local.productos_por_codigo())
        self.stats_text.insert(tk.END, f"  Total: {len(productos)} productos\n")
        
        productos_precio = list(self.local.productos_por_precio())
        if productos_precio:
            self.stats_text.insert(tk.END, f"  Más caro: {productos_precio[-1].nombre}\n")
            self.stats_text.insert(tk.END, f"  Más barato: {productos_precio[0].nombre}\n")
        
        self.stats_text.insert(tk.END, f"\n🌳 Árbol AVL:\n")
        self.stats_text.insert(tk.END, f"  Altura: {self.local.catalogo.altura()}\n")
        self.stats_text.insert(tk.END, f"  Nodos: {len(self.local.catalogo)}\n")
    
    def actualizar_despachados(self):
        self.despachados_listbox.delete(0, tk.END)
        if not self.local.listos:
            self.despachados_listbox.insert(tk.END, "Sin pedidos")
            return
        
        for p in self.local.listos:
            linea = f"#{p.id} {p.cliente:<15} {self.formato_precio(p.total()):>8}  ({p.repartidor or 'Retira'})"
            self.despachados_listbox.insert(tk.END, linea)
    
    def actualizar_estructura(self):
        estructura_nombre = self.estructura_var.get()
        info = info_estructura(estructura_nombre)
        
        self.estructura_text.delete(1.0, tk.END)
        
        if not info:
            return
        
        self.estructura_text.insert(tk.END, f"{'='*60}\n{estructura_nombre}\n{'='*60}\n\n")
        self.estructura_text.insert(tk.END, f"Descripción:\n{info['descripcion']}\n\n")
        self.estructura_text.insert(tk.END, f"Operaciones:\n{info['operacion']}\n\n")
        self.estructura_text.insert(tk.END, "COMPLEJIDAD:\n")
        self.estructura_text.insert(tk.END, f"  O: {info['big_o']}\n")
        self.estructura_text.insert(tk.END, f"  Θ: {info['theta']}\n")
        self.estructura_text.insert(tk.END, f"  Ω: {info['omega']}\n\n")
        self.estructura_text.insert(tk.END, "Usos:\n")
        for uso in info['usos']:
            self.estructura_text.insert(tk.END, f"  • {uso}\n")
    
    def cargar_demo(self):
        try:
            self.local.iniciar_pedido("Ana", "Norte")
            for codigo in (101, 103, 104, 104):
                self.local.agregar(codigo)
            self.local.quitar_ultimo()
            self.local.confirmar()
            
            self.local.iniciar_pedido("Beto", "")
            self.local.agregar(105)
            self.local.confirmar(False)
            
            self.local.iniciar_pedido("Cami", "Sur")
            self.local.agregar(102)
            self.local.confirmar(True, 20)
            
            self.local.iniciar_pedido("Dani", "Costanera")
            self.local.agregar(107)
            self.local.confirmar(True, 10)
            
            for _ in range(4):
                self.local.despachar()
                self.total_despachados += 1
            
            self.actualizar_todo()
            messagebox.showinfo("✅ Demo", "4 pedidos cargados y despachados")
            
        except ErrorDeNegocio as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = PedidosGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
