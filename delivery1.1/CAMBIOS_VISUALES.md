# Cambios Visuales - Interfaz Gráfica v2

## Antes vs Después

### ANTES (GUI v1)
```
┌─────────────────────────────────────────────────────┐
│ Sistema de Pedidos - Local de Comidas  1200x700     │
├─────────────────────────┬─────────────────────────┤
│ PEDIDOS EN ESPERA (15)   │ Catálogo / Zonas / ...  │
│ [___][___][___]          │ (Pocas pestañas)        │
│ [Nuevo] [Despachar]      │                         │
│ [Refrescar]              │                         │
│                          │                         │
│ ÚLTIMOS DESPACHADOS (3)  │                         │
│ [___][___][___]          │ (No hay búsquedas)      │
│                          │ (No hay calculadora)    │
│                          │ (No hay info estructuras│
│                          │                         │
└─────────────────────────┴─────────────────────────┘

❌ Problemas:
- No se puede quitar último producto
- No se puede cancelar pedido
- No se puede agregar múltiples unidades
- No hay búsquedas visibles
- No hay calculadora
- No hay forma de ver complejidad
- Pedido atrapado si hay error
- Estadística muestra máximo 3 despachados
```

---

### DESPUÉS (GUI v2)
```
┌──────────────────────────────────────────────────────────────┐
│ Sistema de Pedidos - Local de Comidas      1400x800          │
├───────────────────────────────┬──────────────────────────────┤
│                               │ [Catálogo] [Búsquedas]       │
│ ┌─────────────────────────┐   │ [Calculadora] [Zonas] ...    │
│ │ NUEVO PEDIDO            │   │                              │
│ ├─────────────────────────┤   │  Catálogo (por código):      │
│ │ Cliente: [Ana_____]     │   │  101 Hamburguesa  $5500      │
│ │ Zona: [Norte____]       │   │  102 Hamburguesa  $7500      │
│ │ Código: [101] Qty: [2]  │   │  103 Papas fritas $3000      │
│ │ [Agregar] [Quitar ult]  │   │  104 Gaseosa      $2000      │
│ │ [✓ Confirmar][✗ Cancel] │   │  105 Pizza        $8000      │
│ │ [📊 Cargar Demo]        │   │  ...                         │
│ ├─────────────────────────┤   ├──────────────────────────────┤
│ │ PRODUCTOS DEL PEDIDO    │   │ BÚSQUEDAS:                   │
│ │ 101 Hamburguesa $5500   │   │ Por precio: [3000] [Buscar]  │
│ │ 102 Hamburguesa $7500   │   │ ✓ 103 - Papas fritas        │
│ │ TOTAL: $13000           │   │                              │
│ ├─────────────────────────┤   │ Por nombre: [____] [Buscar]  │
│ │ PEDIDOS EN ESPERA (2)   │   │                              │
│ │ 1. #001 Ana    $13000   │   │ Combo: [13000] [Buscar]      │
│ │ 2. #002 Beto   $5500    │   │ ✓ Hamburguesa + Pizza       │
│ │ [Despachar] [Refrescar] │   ├──────────────────────────────┤
│ │                          │   │ CALCULADORA:                 │
│ │ ÚLTIMOS DESPACHADOS (3) │   │ [(5500+3000)*90/100]         │
│ │ #001 Ana  $13000 (Ana)  │   │ [Calcular]                   │
│ └─────────────────────────┘   │ $7650                        │
│                               └──────────────────────────────┘
└───────────────────────────────┴──────────────────────────────┘

✅ Mejoras:
✓ Panel de armado completo
✓ Quitar último producto (pila)
✓ Cancelar pedido
✓ Múltiples unidades
✓ Búsquedas visibles (binaria, secuencial, backtracking)
✓ Calculadora (postfija)
✓ Información de complejidad
✓ Pedido atrapado se recupera automáticamente
✓ Estadística correcta (total ≠ cola circular)
✓ Botón para cargar demo
✓ 6 pestañas con todas las características
```

---

## Distribución de Espacio

### Panel Izquierdo (Antes)
```
[Pedidos en espera]          50% altura
[Últimos despachados]        25% altura
[Botones]                     5% altura
```

### Panel Izquierdo (Después)
```
[Formulario armado]           20% altura
[Productos del pedido]        15% altura
[Total]                        5% altura
[Pedidos en espera]           35% altura
[Botones despacho]             5% altura
[Últimos despachados]         20% altura
```

---

## Nuevas Pestañas

```
┌─ Catálogo ────────┐
│ Todos los         │  ABB/AVL ordenado
│ productos por     │  por código
│ código            │
└───────────────────┘

┌─ Búsquedas ───────┐
│ • Por precio      │  Binaria O(log n)
│ • Por nombre      │  Secuencial O(n)
│ • Combo           │  Backtracking O(2^n)
└───────────────────┘

┌─ Calculadora ─────┐
│ Expresión:        │  Notación postfija
│ (5500 + 3000)...  │  Usa pila
│ Resultado: $7650  │
└───────────────────┘

┌─ Zonas ───────────┐
│ Mapa de rutas     │  Grafo
│ BFS / DFS         │  Matriz adyacencia
│ Rutas cortas      │
└───────────────────┘

┌─ Estadísticas ────┐
│ Pedidos en espera │  Métricas
│ Total despachados │  Árbol AVL
│ En pizarra        │  Repartidores
└───────────────────┘

┌─ Estructuras ─────┐
│ [Pila ▼]          │  16 estructuras
│ Descripción...    │  Complejidad O/Θ/Ω
│ O(1) Θ(1) Ω(1)   │  Usos en proyecto
└───────────────────┘
```

---

## Flujo de Uso Mejorado

### Antes
```
Usuario
  ↓
[Crear pedido]
  ↓
[Agregar producto (solo 1 código)]
  ↓
[Confirmar]
  ↓
[Ver en lista]
  ↓
[Despachar]
  ↓
[Ver en últimos 3]

❌ No se puede:
  - Agregar múltiples unidades
  - Quitar producto
  - Cancelar
  - Buscar
  - Calcular
  - Ver complejidad
```

### Después
```
Usuario
  ├─ ARMAR PEDIDO
  │  ├─ [Cliente][Zona]
  │  ├─ [Código] [Cantidad] [Agregar]
  │  ├─ [Quitar último]
  │  ├─ [Urgencia] [Minutos]
  │  └─ [Confirmar] o [Cancelar]
  │
  ├─ VER EN ESPERA
  │  ├─ (Urgentes primero)
  │  ├─ (Normales FIFO)
  │  └─ [Despachar siguiente]
  │
  ├─ EXPLORAR CARACTERÍSTICAS
  │  ├─ BÚSQUEDAS
  │  │  ├─ Binaria por precio
  │  │  ├─ Secuencial por nombre
  │  │  └─ Backtracking combo
  │  │
  │  ├─ CALCULADORA
  │  │  └─ Evaluar postfija
  │  │
  │  ├─ ZONAS
  │  │  ├─ Mapa de rutas
  │  │  ├─ BFS/DFS
  │  │  └─ Rutas más cortas
  │  │
  │  └─ ESTADÍSTICAS
  │     ├─ Total despachados (correcto)
  │     ├─ Cola circular (últimos 3)
  │     └─ Árbol AVL
  │
  └─ INFORMACIÓN
     ├─ Complejidad O/Θ/Ω
     ├─ 16 estructuras
     └─ Usos en proyecto

✓ Todo accesible y funcional
```

---

## Dimensiones

| Elemento | Antes | Después | Cambio |
|----------|-------|---------|--------|
| Ventana | 1200x700 | 1400x800 | +200x100 (más espacio) |
| Panel izq | 50% | 40% | Más compacto |
| Panel der | 50% | 60% | Más información |
| Botones | 3 | 7+ | Más acciones |
| Pestañas | 4 | 6 | 50% más |

---

## Accesibilidad

### Antes
```
❌ Botón "Quitar último"        NO VISIBLE
❌ Opción "Cancelar pedido"     NO VISIBLE
❌ Búsqueda binaria             NO VISIBLE
❌ Búsqueda secuencial          NO VISIBLE
❌ Búsqueda backtracking        NO VISIBLE
❌ Calculadora                  NO VISIBLE
❌ Información estructuras      SOLO EN PEQUEÑO DROPDOWN
```

### Después
```
✅ Botón "Quitar último"        VISIBLE - Panel izq
✅ Botón "Cancelar pedido"      VISIBLE - Panel izq
✅ Búsqueda binaria             VISIBLE - Pestaña Búsquedas
✅ Búsqueda secuencial          VISIBLE - Pestaña Búsquedas
✅ Búsqueda backtracking        VISIBLE - Pestaña Búsquedas
✅ Calculadora                  VISIBLE - Pestaña Calculadora
✅ Información estructuras      VISIBLE - Pestaña Estructuras
✅ Formulario con spinbox       VISIBLE - Panel izq
✅ Múltiples unidades           VISIBLE - Spinbox
✅ Checkbox urgencia            VISIBLE - Panel izq
✅ Entrada de minutos           VISIBLE - Panel izq
```

---

## Mejoras de UX

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Flujo de armado** | Incompleto | Completo y lineal |
| **Validación** | Básica | Con recuperación automática |
| **Información visual** | Mínima | Abundante |
| **Accesibilidad** | 40% funciones | 100% funciones |
| **Número de clicks** | Más | Menos (todo visible) |
| **Exploración** | Difícil | Fácil (pestañas claras) |
| **Demostración** | Manual | Automática (botón demo) |
| **Complejidad** | Oculta | Visible (pestaña dedic.) |

---

## Resumen Visual

### Cambio más importante
**Panel de armado reorganizado**
- Antes: Desparramado, incompleto
- Después: Lineal, intuitivo, con spinbox y múltiples opciones

### Cambio más útil
**6 Pestañas**
- Antes: 4 pestañas básicas
- Después: Todo lo necesario visible y organizado

### Cambio más visible
**Botón "📊 Cargar Demo"**
- Antes: Demo solo en modo consola
- Después: Un click carga datos reales

### Cambio más importante para TP
**Pestaña "Estructuras"**
- Muestra todas las 16 estructuras
- Con complejidad O/Θ/Ω
- Explicación de usos en proyecto

