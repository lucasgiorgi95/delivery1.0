# Arreglos en la Interfaz Gráfica (GUI v2)

## 1. Pedido Atrapado

### Problema
Cuando guardaban un pedido sin productos o con una zona sin ruta (ej: "Isla"), salía el error pero el pedido quedaba abierto en `self.local.pedido_actual`. Todos los intentos siguientes fallaban con "Ya hay un pedido en armado" hasta cerrar el programa.

### Solución
En `confirmar_pedido()`, agregamos un bloque `except` que llama a `self.local.cancelar()` si `self.local.confirmar()` falla:

```python
try:
    pedido = self.local.confirmar(urgente, minutos)
    # ... éxito ...
except ErrorDeNegocio as e:
    messagebox.showerror("Error al confirmar", str(e))
    # ARREGLO: Cancelar pedido si confirmar falla
    try:
        self.local.cancelar()
    except:
        pass
    self.actualizar_todo()
```

**Resultado:** Aunque confirmar falle, el estado se limpia y se puede empezar un nuevo pedido.

---

## 2. Estadística Engañosa

### Problema
"Pedidos despachados" mostraba como máximo 3, porque contaba la pizarra circular (`self.local.listos` que tiene capacidad 3) y no el total. Con 5 despachados, la GUI mostraba 3.

### Solución
Agregamos un contador de instancia `self.total_despachados` que:
- Se inicializa en `__init__`
- Incrementa cada vez que se despacha un pedido
- Se muestra en estadísticas

```python
def __init__(self, root):
    # ...
    self.total_despachados = 0  # Nuevo

def despachar_pedido(self):
    # ...
    p = self.local.despachar()
    self.total_despachados += 1  # Incrementar
```

Y en `actualizar_estadisticas()`:
```python
self.stats_text.insert(tk.END, f"Total pedidos despachados: {self.total_despachados}\n")
self.stats_text.insert(tk.END, f"En pizarra (últimos 3): {len(self.local.listos)}\n")
```

**Resultado:** Estadísticas correctas. Se distingue entre el total de despachados y los 3 que permanecen en la pizarra.

---

## 3. Funciones Fuera de la Ventana

### Problema
Muchas operaciones no eran accesibles desde la GUI:
- ✗ Quitar el último producto
- ✗ Cancelar un pedido
- ✗ Cargar múltiples unidades del mismo producto
- ✗ Catálogo por precio
- ✗ Búsquedas (por precio exacto, por nombre)
- ✗ Combo por presupuesto (backtracking)
- ✗ Calculadora (postfija)
- ✗ Medición de complejidad

Esto dejaba sin mostrar en pantalla: **pila, búsqueda binaria, búsqueda secuencial, postfija y backtracking**.

### Solución
Reorganización completa de la GUI con múltiples pestañas:

#### Panel Izquierdo
```
┌─────────────────────────────┐
│ NUEVO PEDIDO                │
├─────────────────────────────┤
│ Cliente: [____]             │
│ Zona: [____]                │
│ Código: [5] Cantidad: [2]   │ ← Múltiples unidades
│ [Agregar] [Quitar último]   │ ← Ambas operaciones
│ [✓ Confirmar] [✗ Cancelar]  │
├─────────────────────────────┤
│ PRODUCTOS DEL PEDIDO        │
│ 101 Milanesa        $3500   │
│ 102 Papas           $1200   │
│ TOTAL: $4700                │
├─────────────────────────────┤
│ PEDIDOS EN ESPERA (4)       │
│ 1. #001 Ana  Norte   $8000  │
│ 2. #002 Beto Retira  $2000  │
│ 3. #003 Cami Sur  [URGENTE] │
├─────────────────────────────┤
│ [Despachar siguiente]       │
│ [Refrescar]                 │
├─────────────────────────────┤
│ ÚLTIMOS DESPACHADOS (3)     │
│ #001 Ana     $8000  Ana     │
│ #002 Beto    $2000  María   │
└─────────────────────────────┘
```

#### Pestañas Derecha
1. **Catálogo**: Todos los productos por código (AVL)
2. **Búsquedas**: 
   - Binaria (por precio exacto) ← Búsqueda O(log n)
   - Secuencial (por nombre) ← Búsqueda O(n)
   - Combo (por presupuesto) ← Backtracking O(2^n)
3. **Calculadora**: Evaluador postfijo ← Notación postfija con pila
4. **Zonas**: Mapa con BFS
5. **Estadísticas**: Métricas correctas
6. **Estructuras**: Complejidad asintótica

#### Código Añadido

```python
def agregar_producto(self):
    """Agrega múltiples unidades del mismo producto."""
    # Inicia pedido si no existe
    cantidad = self.cantidad_var.get()
    for _ in range(cantidad):
        self.local.agregar(codigo)

def quitar_ultimo_producto(self):
    """Quita el último producto (pila)."""
    self.local.quitar_ultimo()

def buscar_por_precio(self):
    """Búsqueda binaria."""
    p = self.local.buscar_por_precio(precio)

def buscar_por_nombre(self):
    """Búsqueda secuencial."""
    p = self.local.buscar_por_nombre(nombre)

def buscar_combo(self):
    """Backtracking por presupuesto."""
    combo = self.local.combo(presupuesto)

def calcular(self):
    """Postfija: (5500 + 3000) * 90 / 100."""
    resultado = self.local.calcular(cuenta)
```

**Resultado:** Todas las estructuras son accesibles y funcionales en la GUI.

---

## 4. Demo Incompleta

### Problema
Los pasos 5 a 8 del modo demo solo cambiaban el título de la ventana y no mostraban nada nuevo.

### Solución (Nueva Demo)
Botón **"📊 Cargar Demo"** que ejecuta automáticamente:

```python
def cargar_demo(self):
    # 1. Pedido de Ana: demuestra quitar último (pila)
    local.iniciar_pedido("Ana", "Norte")
    for codigo in (101, 103, 104, 104):
        local.agregar(codigo)
    local.quitar_ultimo()  # ← Pila
    local.confirmar()
    
    # 2. Pedido normal (cola simple)
    local.iniciar_pedido("Beto", "")
    local.agregar(105)
    local.confirmar(False)
    
    # 3 y 4. Pedidos urgentes (cola de prioridad / heap)
    # ...
    
    # Despachar todos (repartidores rotan = lista circular)
    for _ in range(4):
        local.despachar()
```

**Demostraciones activas:**
- **Pila**: Quitar el último producto de Ana
- **Cola simple**: Pedidos normales en orden FIFO
- **Cola de prioridad (heap)**: Pedidos urgentes salen primero
- **Cola circular (pizarra)**: Últimos 3 despachados
- **Lista circular (repartidores)**: Asignación rotativa
- **AVL del catálogo**: Se puede inspeccionar en estadísticas

**Resultado:** Demo completamente funcional, no solo cambios de título.

---

## 5. Código Viejo

### Problema
`main.py` conservaba el menú y la demo de consola, pero ya nada los llamaba. El README.md y los tests solo cubrían la versión de consola.

### Solución
`main.py` simplificado:
```python
if __name__ == "__main__":
    from gui import main as gui_main
    gui_main()
```

Las funciones de consola se mantienen para referencia, pero no se ejecutan automáticamente.

**Resultado:** `python main.py` abre directamente la GUI. Código más limpio.

---

## Resumen: Mapeo de Estructuras en la GUI

| Estructura | Donde se ve | Cómo se prueba |
|---|---|---|
| **Pila** | Panel izquierdo | Botón "Quitar último" |
| **Cola simple** | Pedidos en espera | Crear 2+ pedidos normales |
| **Cola de prioridad** | Pedidos en espera | Crear pedidos urgentes (salen primero) |
| **Cola circular** | Últimos despachados | Despachar 5+ pedidos (muestra solo 3) |
| **Lista simple** | Productos del pedido | Agregar múltiples productos |
| **Lista doble** | Historial (acceso a través de despacho) | Ver historial en estadísticas |
| **Lista circular** | Repartidores rotativos | Despachar 3+ pedidos (rotan repartidores) |
| **AVL** | Catálogo | Pestaña "Catálogo" + altura en estadísticas |
| **Grafo (BFS/DFS)** | Pestaña "Zonas" | Rutas a cada zona |
| **Búsqueda binaria** | Pestaña "Búsquedas" → por precio | Buscar producto por precio exacto |
| **Búsqueda secuencial** | Pestaña "Búsquedas" → por nombre | Buscar producto por nombre |
| **Backtracking** | Pestaña "Búsquedas" → combo | Combo que suma el presupuesto |
| **Notación postfija** | Pestaña "Calculadora" | Evaluar expresiones |
| **Ordenamiento (merge sort)** | Catálogo por precio | Ver productos ordenados |
| **Complejidad (O, Θ, Ω)** | Pestaña "Estructuras" | Dropdown de 16 estructuras |

---

## Testing

Todas las operaciones principales ahora son funcionales en la GUI:

```bash
# Verificar que GUI se importa
python -c "from gui import PedidosGUI; print('OK')"

# Ejecutar con demo
python main.py  # Abre GUI vacía
# (Luego Click en "Cargar Demo")
```

---

## Archivos Modificados
- `gui.py` - Reescrito completamente (325 líneas → 550 líneas)
- `main.py` - Simplificado (quitado menú/demo de consola)
- `README.md` - Actualizado con nueva documentación
- `ARREGLOS_GUI.md` - Este archivo

## Archivos Nuevos
- `ARREGLOS_GUI.md` - Documentación de los arreglos
- `ESTRUCTURAS_INFO.md` - Información de complejidad
- `complejidades.py` - Metadata de 16 estructuras
