# Cómo Usar el Sistema de Pedidos v2

## Inicio Rápido

### Opción 1: Interfaz Gráfica (Recomendado)
```bash
python main.py
```

Esto abre una ventana con la interfaz gráfica completa.

### Opción 2: Cargar Datos de Demostración
1. Ejecutar `python main.py`
2. En el panel izquierdo, buscar botón **"📊 Cargar Demo"**
3. Click en ese botón
4. Se cargarán automáticamente 4 pedidos de ejemplo

### Opción 3: Tests
```bash
python -m unittest discover tests
python test_arreglos.py
```

---

## Interfaz Gráfica - Guía Completa

### Panel Izquierdo: Armado de Pedidos

#### 1. Crear un Nuevo Pedido
```
┌─────────────────────────────┐
│ NUEVO PEDIDO                │
├─────────────────────────────┤
│ Cliente: [Ana____]          │ ← Nombre del cliente (requerido)
│ Zona: [Norte_____]          │ ← Zona (Enter si retira en local)
│ Código: [101] Cantidad: [2] │ ← Código + unidades
│ [Agregar] [Quitar último]   │
└─────────────────────────────┘
```

**Pasos:**
1. Ingresa nombre del cliente en "Cliente"
2. Ingresa zona de entrega (o deja vacío para "Retira en el local")
3. Ingresa código de producto y cantidad
4. Click en **"Agregar"**

#### 2. Quitar el Último Producto
Si cometiste un error:
1. Click en **"Quitar último"**
2. Se elimina el último producto agregado (demuestra **pila**)

#### 3. Marcar como Urgente
```
[✓] ¿Es urgente?
Minutos promesa: [15]
```

Si es urgente:
1. Marca el checkbox "¿Es urgente?"
2. Ingresa minutos promesa (ej: 20, 10)
3. El pedido saldrá primero en despacho (demuestra **cola de prioridad**)

#### 4. Confirmar o Cancelar
- **[✓ Confirmar]**: Guarda el pedido y empieza uno nuevo
- **[✗ Cancelar]**: Descarta todo y limpia el formulario

**Importante:** Si confirmar falla (ej: sin productos, zona inválida), el pedido se cancela automáticamente y puedes intentar de nuevo.

#### 5. Ver Productos Cargados
```
┌──────────────────────────────┐
│ PRODUCTOS DEL PEDIDO         │
├──────────────────────────────┤
│ 101 Hamburguesa simple $5500 │
│ 102 Hamburguesa doble  $7500 │
│ TOTAL: $13000               │
└──────────────────────────────┘
```

Se actualiza automáticamente al agregar/quitar productos.

### Panel Izquierdo: Despacho

#### 6. Ver Pedidos en Espera
```
┌──────────────────────────────────┐
│ PEDIDOS EN ESPERA                │
├──────────────────────────────────┤
│ 1. #001 Ana      Norte   $13000  │
│ 2. #002 Beto     Retira   $5500  │ (normal)
│ 3. #003 Cami     Sur      $3000  │ (urgente)
│ 4. #004 Dani  Costanera   $3500  │ (urgente)
└──────────────────────────────────┘
```

**Orden:** Urgentes primero (por minutos promesa), luego normales (FIFO).

#### 7. Despachar Pedidos
Click en **"Despachar siguiente"**:
- Sale el primer pedido de la lista (urgente o normal)
- Se asigna un repartidor automáticamente
- Aparece en "Últimos despachados"

#### 8. Ver Últimos Despachados
```
┌──────────────────────────────────┐
│ ÚLTIMOS DESPACHADOS (3)          │
├──────────────────────────────────┤
│ #001 Ana     $13000  (Ana)       │
│ #002 Beto     $5500  (Retira)    │
│ #003 Cami     $3000  (María)     │
└──────────────────────────────────┘
```

Se muestran los últimos 3 (demuestra **cola circular**).

---

## Pestañas Derecha: Operaciones Avanzadas

### Pestaña 1: Catálogo
```
PRODUCTOS (por código)
101 Hamburguesa simple     $5500
102 Hamburguesa doble      $7500
103 Papas fritas           $3000
104 Gaseosa                $2000
105 Pizza muzzarella       $8000
106 Helado                 $2500
107 Cerveza                $3500
```

Muestra todos los productos ordenados por código (demuestra **ABB/AVL**).

---

### Pestaña 2: Búsquedas

#### Búsqueda Binaria (por precio exacto) - O(log n)
```
Producto por precio exacto:
[3000] [Buscar]
✓ 103 - Papas fritas ($3000)
```

**Cómo:** Ingresa precio exacto, click en "Buscar".

#### Búsqueda Secuencial (por nombre) - O(n)
```
Producto por nombre:
[Hamburguesa simple] [Buscar]
✓ 101 - Hamburguesa simple ($5500)
```

**Cómo:** Ingresa nombre exacto (case-sensitive), click en "Buscar".

#### Combo por Presupuesto - O(2^n) Backtracking
```
Combo por presupuesto:
[13000] [Buscar]
✓ Hamburguesa simple, Hamburguesa doble, Pizza muzzarella = $21000
```

**Cómo:** Ingresa presupuesto, click en "Buscar".
Encuentra una combinación de productos que sume exactamente ese presupuesto.

---

### Pestaña 3: Calculadora (Notación Postfija)

```
Evaluar cuenta (postfija)
Ejemplo: (5500 + 3000) * 90 / 100
[(5500 + 3000) * 90 / 100] [Calcular]
$7650
```

**Cómo:** Ingresa una expresión matemática.
- Soporta: + - * / paréntesis
- Se convierte internamente a postfija y se evalúa (demuestra **pila**)

---

### Pestaña 4: Zonas

```
Zonas alcanzables:
Centro, Norte, Sur, Costanera

Recorrido BFS:
Local -> Centro -> Norte -> Sur -> Costanera

Rutas más cortas:
  Centro: Local -> Centro
  Norte: Local -> Centro -> Norte
  Sur: Local -> Centro -> Sur
  Costanera: Local -> Sur -> Costanera
```

Muestra el mapa de entregas (demuestra **grafo con BFS/DFS**).

---

### Pestaña 5: Estadísticas

```
ESTADÍSTICAS DEL SISTEMA
==================================================
Pedidos en espera: 2
Dinero en espera: $8500
Total pedidos despachados: 5          ← Correcto: total acumulado
En pizarra (últimos 3): 3            ← Cola circular: solo últimos 3

Catálogo:
  Total de productos: 7
  Más caro: Pizza muzzarella ($8000)
  Más barato: Gaseosa ($2000)

Árbol AVL del catálogo:
  Altura: 3
  Nodos: 7

Repartidores disponibles: 3
```

Muestra todas las métricas importantes, incluyendo la **diferencia correcta** entre total despachados y cola circular.

---

### Pestaña 6: Estructuras

```
Ver complejidad de: [Pila ▼]
============================================================
Pila
============================================================

Descripción:
Última entrada, primera salida (LIFO)

Operaciones principales:
apilar, desapilar

COMPLEJIDAD ASINTÓTICA:
  Big O (peor caso):     O(1)
  Theta (promedio):      Θ(1)
  Omega (mejor caso):    Ω(1)

Usos en este local:
  • Quitar el último producto del pedido
  • Combo por presupuesto (backtracking)
  • Calculadora postfija
```

**Cómo:** Selecciona una estructura del dropdown para ver:
- Descripción
- Operaciones principales
- Complejidad asintótica (O, Θ, Ω)
- Dónde se usa en el local

**Estructuras disponibles (16):**
1. Pila
2. Cola
3. Cola de Prioridad (Heap)
4. Lista Simple
5. Lista Doble
6. Lista Circular
7. Árbol Binario de Búsqueda (ABB)
8. Árbol AVL
9. Grafo - Lista de Adyacencia
10. Ordenamiento - Merge Sort
11. Ordenamiento - Bubble Sort
12. Ordenamiento - Quick Sort
13. Búsqueda Secuencial
14. Búsqueda Binaria
15. Backtracking
16. Notación Postfija

---

## Ejemplos de Uso

### Ejemplo 1: Crear un Pedido Normal
1. Cliente: "Ana"
2. Zona: "Norte"
3. Agregar: 101 x1, 103 x2
4. Click en "✓ Confirmar"
→ Pedido #1 confirmado, aparece en "Pedidos en espera"

### Ejemplo 2: Crear un Pedido Urgente
1. Cliente: "Beto"
2. Zona: "" (retira)
3. Agregar: 105 x1
4. Marcar "¿Es urgente?" y poner "10" minutos
5. Click en "✓ Confirmar"
→ Pedido #2 confirmado, saldrá primero al despachar

### Ejemplo 3: Despachar Pedidos
1. Click en "Despachar siguiente" (sale Beto urgente)
2. Click en "Despachar siguiente" (sale Ana normal)
3. Mostrar "Últimos despachados": primeros 3

### Ejemplo 4: Buscar Combo
1. Ir a pestaña "Búsquedas"
2. Ingresar presupuesto: 13000
3. Click en "Buscar"
→ Muestra: Hamburguesa simple + Hamburguesa doble + Pizza

### Ejemplo 5: Calcular Promedio
1. Ir a pestaña "Calculadora"
2. Ingresar: (5500 + 3000) * 90 / 100
3. Click en "Calcular"
→ Resultado: $7650

### Ejemplo 6: Cargar Demo Completa
1. Click en "📊 Cargar Demo"
2. Se cargan 4 pedidos automáticamente
3. Se despachan todos
4. Se pueblan todas las vistas con datos reales

---

## Troubleshooting

### "Ya hay un pedido en armado"
→ Click en "✗ Cancelar" para limpiar

### Confirmar falla pero no se limpia el pedido
→ Se limpia automáticamente. Intenta de nuevo.

### Búsqueda retorna "No encontrado"
→ Verifica el nombre exacto (case-sensitive) o precio exacto

### Combo retorna "Sin combinación exacta"
→ No hay una combinación que sume justo ese presupuesto

### No veo los últimos despachados
→ Despacha más pedidos (la cola circular muestra máximo 3)

---

## Archivos Relacionados

- `README.md` - Descripción general del proyecto
- `ESTRUCTURAS_INFO.md` - Información detallada de complejidad
- `ARREGLOS_GUI.md` - Qué se arregló en esta versión
- `RESUMEN_CAMBIOS.md` - Resumen técnico de cambios
- `test_arreglos.py` - Tests de validación

---

## Atajos Útiles

| Acción | Atajo |
|--------|-------|
| Refrescar vistas | Click "Refrescar" o cambiar pestaña |
| Limpiar formulario | Click "✗ Cancelar" |
| Ver complejidad | Ir a pestaña "Estructuras" y seleccionar |
| Cargar datos de ejemplo | Click "📊 Cargar Demo" |

---

**¿Necesitas ayuda?** Consulta `README.md` o revisa los archivos de documentación.
