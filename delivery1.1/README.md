# 🍕 Pedidos de un Local de Comidas - v2.0

**Sistema integral de pedidos** | Estructura de Datos (TP Integrador) | Python 3

Programa educativo que implementa **9 estructuras de datos** resolviendo problemas reales de un local de comidas: armado de pedidos, colas de espera, despacho con prioridades, gestión de rutas, búsquedas y análisis de complejidad.

---

## 🎯 Características principales

✅ **Interfaz gráfica mejorada (v2.0)**
- Panel de armado de pedidos con validación en tiempo real
- 4 pestañas temáticas (refactorizado): Catálogo, Zonas, Estadísticas, Estructuras
- Demo automática cargable en un click
- Todos los problemas de v1 solucionados

✅ **9 estructuras implementadas manualmente**
- Pilas, Colas, Colas de Prioridad, Listas (simple, doble, circular)
- Árboles (ABB, AVL), Grafos (BFS, DFS)
- Sin librerías externas (heapq, deque, isect)

✅ **Algoritmos educativos**
- Ordenamiento: Burbuja, Selección, Inserción, Shell, Quicksort, Mergesort
- Búsqueda: Secuencial O(n), Binaria O(log n), Backtracking O(2^n)
- Postfija, Complejidad medida

✅ **Medición de complejidad real**
- Menú 8: Tiempos reales de ordenamiento
- Comparación: ABB vs AVL, búsqueda secuencial vs binaria
- Tabla interactiva

---

## 🚀 Cómo ejecutar

### GUI (Recomendado)
\\\ash
python main.py
\\\

### Demo automática en consola
\\\ash
python main.py --demo
\\\

### Tests
\\\ash
python test_arreglos.py          # Tests de los arreglos v2.0
python -m unittest discover tests # 32 tests del proyecto original
\\\

---

## 🎮 Interfaz Gráfica v2.0

### Panel Izquierdo - Armado de Pedidos

| Sección | Función |
|---------|---------|
| **Formulario superior** | Cliente, Zona, Código+Cantidad, ¿Urgente?, Minutos |
| **Productos cargados** | Lista con nombre, precio, cantidad y subtotal |
| **Botones de acción** | Agregar, Quitar último (pila), Confirmar, Cancelar |
| **Pedidos en espera** | Lista ordenada: urgentes primero (cola de prioridad) |
| **Panel de despacho** | «Despachar siguiente» + últimos 3 despachados |

### Pestañas

#### 📋 **Catálogo**
- Productos ordenados por código (árbol AVL)
- Visualización: código, nombre, precio
- Estructura: Árbol Binario de Búsqueda (ABB/AVL)

#### 🔍 **Búsquedas**
- **Binaria por precio exacto** O(log n) — catálogo ordenado
- **Secuencial por nombre** O(n) — búsqueda simple
- **Combo por presupuesto** O(2^n) — backtracking con pila

#### 🧮 **Calculadora**
- Evaluador de expresiones postfijas
- Entrada: \(5500+3000)*90/100\
- Conversión interna: infija → postfija
- Salida: \

#### 🗺️ **Zonas**
- Mapa de rutas entre zonas (grafo con lista de adyacencia)
- **BFS**: Ruta con menos paradas hasta una zona
- **DFS**: Qué zonas se pueden alcanzar desde el local
- Conexiones: Local → Norte, Sur, Costanera, Isla

#### 📊 **Estadísticas**
- Total de pedidos creados
- Total dinero procesado
- Total pedidos despachados (contador persistente)
- Últimos 3 despachados (cola circular)
- Altura del árbol AVL de catálogo

#### 🏗️ **Estructuras**
- Dropdown con 9 estructuras disponibles
- Cada una muestra:
  - Descripción y operación principal
  - Big O (peor caso)
  - Theta (promedio)
  - Omega (mejor caso)
  - Usos en el local

---

## 🛠️ Problemas Solucionados en v2.0

### 1️⃣ Pedido Atrapado
**Problema:** Si confirmar() fallaba (sin productos o zona sin ruta), el pedido quedaba abierto.
**Solución:** Llamar automáticamente a cancelar() si confirmar() falla.

### 2️⃣ Estadística Engañosa
**Problema:** «Total despachados» mostraba máximo 3 (cola circular).
**Solución:** Contador 	otal_despachados persistente que no se vacía.

### 3️⃣ Funciones Fuera de Ventana
**Problema:** No cabían en pantalla: quitar último, cancelar, múltiples unidades, búsquedas, combo, calculadora.
**Solución:** Reorganización completa: panel izquierdo + 6 pestañas temáticas.

### 4️⃣ Demo Incompleta
**Problema:** Pasos 5-8 solo cambiaban título sin hacer nada.
**Solución:** Método cargar_demo() que crea 4 pedidos reales y los despacha automáticamente.

### 5️⃣ Código Viejo
**Problema:** main.py tenía menú de consola sin usar.
**Solución:** main.py simplificado, solo llama a gui.main().

---

## 📁 Estructura del Proyecto

\\\
delivery1.1/
├── main.py                      Punto de entrada (GUI)
├── gui.py                       Interfaz gráfica Tkinter (550 líneas)
├── local.py                     Lógica de negocio (sin I/O)
├── modelos.py                   Clases Producto y Pedido
├── medir.py                     Mediciones de complejidad
├── complejidades.py             Metadata de 9 estructuras
│
├── estructuras/
│   ├── nodo.py                  Nodo autorreferenciado (base de todo)
│   ├── pila.py                  Pila dinámica (para «quitar último»)
│   ├── cola.py                  Cola simple + circular
│   ├── cola_prioridad.py        Heap (para pedidos urgentes)
│   ├── listas.py                Simple, doble, circular
│   ├── arbol.py                 ABB + AVL con rotaciones
│   ├── grafo.py                 Lista de adyacencia, BFS, DFS
│   └── __init__.py
│
├── algoritmos/
│   ├── ordenamiento.py          6 algoritmos de orden O(n²) y O(n log n)
│   ├── busqueda.py              Secuencial, binaria, en árbol
│   ├── postfija.py              Evaluador de notación postfija
│   ├── backtracking.py          Combo por presupuesto
│   └── __init__.py
│
├── test_arreglos.py             Tests de los arreglos v2.0 (3 tests)
├── test_todo.py                 Tests adicionales
│
└── docs/
    ├── README.md                Este archivo
    ├── PROYECTO_COMPLETADO.txt  Resumen técnico v2.0
    ├── COMO_USAR.md             Guía de usuario (paso a paso)
    ├── ESTRUCTURAS_INFO.md      Info detallada de 9 estructuras
    └── MAPEO_ESTRUCTURAS_GUI.md Qué estructura usa cada pestaña
\\\

---

## 📚 Mapa: Programa de Materia → Ubicación → Uso

| Unidad | Tema | Archivo | En el Local |
|--------|------|---------|-----------|
| 1 | TAD | modelos.py | Producto y Pedido como cajas negras |
| 1 | Complejidad Big O | medir.py | Menú: tiempos reales |
| 2 | Nodos autorreferenciados | 
odo.py | Base de pilas, colas, listas |
| 3 | **Pila** | pila.py | Quitar el último producto |
| 3 | Notación postfija | postfija.py | Calculadora: (5500+3000)*90/100 |
| 3 | Backtracking | acktracking.py | Combo por presupuesto |
| 3 | **Cola simple** | cola.py | Pedidos normales (FIFO) |
| 3 | **Cola circular** | cola.py | Pizarra «últimos 3 despachados» |
| 3-7 | **Cola de prioridad** | cola_prioridad.py | Pedidos urgentes (heap) |
| 4 | **Lista simple** | listas.py | Productos del pedido |
| 4 | **Lista doble** | listas.py | Historial de pedido (ambos sentidos) |
| 4 | **Lista circular** | listas.py | Turnos rotativos de repartidores |
| 5 | 6 Ordenamientos | ordenamiento.py | Catálogo por precio (mergesort) |
| 6 | Búsqueda secuencial | usqueda.py | Por nombre (O(n)) |
| 6 | Búsqueda binaria | usqueda.py | Por precio exacto (O(log n)) |
| 7 | **Árbol binario** | rbol.py | Catálogo por código |
| 7 | **ABB** | rbol.py | Búsqueda ordenada |
| 7 | **AVL** (introducción) | rbol.py | Balanceo automático con rotaciones |
| 8 | **Grafo** | grafo.py | Mapa de zonas |
| 8 | **BFS** | grafo.py | Ruta con menos paradas |
| 8 | **DFS** | grafo.py | Qué zonas se alcanzan |

---

## ✅ Validación y Testing

### Tests Implementados
\\\ash
Test 1: Pedido atrapado se recupera
  ✓ Error confirmar sin productos → cancelar() automático

Test 2: Estadística correcta
  ✓ Total despachados persiste (no solo cola circular)

Test 3: Todas las operaciones
  ✓ Múltiples unidades del mismo producto
  ✓ Quitar último (pila)
  ✓ Búsqueda binaria O(log n)
  ✓ Búsqueda secuencial O(n)
  ✓ Combo por presupuesto O(2^n)
  ✓ Calculadora postfija
  ✓ Zonas y BFS

Resultado: ✓ TODOS PASARON
\\\

---

## 🎓 Cosas Importantes (para la Explicación)

- ✅ **Sin librerías externas:** heapq, deque, isect están prohibidos.
- ✅ **Estructuras propias:** Nodo, Pila, Cola, Heap, Listas, ABB, AVL, Grafo: 100% implementado.
- ✅ **Dinámicas:** Pila usa nodos dinámicos; cola también.
- ✅ **Heap en array:** ColaPrioridad usa arreglo, no nodos.
- ✅ **AVL no es masivo:** Es la introducción, con O(log n) en operaciones.
- ✅ **Backtracking O(2^n):** Con 7 productos no se nota, pero es exponencial en el peor caso.
- ✅ **Datos volátiles:** Al cerrar, se pierden los pedidos (no hay persistencia).
- ✅ **ListaSimple.insertar_final O(n):** A propósito. Con cola de punteros sería O(1).

---

## 👥 Reparto sugerido (de a 2)

| Persona A | Persona B | Juntos |
|-----------|-----------|--------|
| Pilas | Árboles (ABB/AVL) | local.py |
| Colas | Grafos | main.py |
| Cola de Prioridad | Ordenamiento | Pruebas |
| Listas | Búsqueda | Explicación final |
| modelos.py | medir.py | Demo |
| Postfija | | |
| Backtracking | | |

**Nota:** Cada uno debe poder explicar también las piezas del otro. Son interdependientes.

---

## 📖 Documentación Completa

- **COMO_USAR.md** — Guía paso a paso de la interfaz gráfica
- **ESTRUCTURAS_INFO.md** — Detalles de 9 estructuras + complejidad O/Θ/Ω
- **MAPEO_ESTRUCTURAS_GUI.md** — Qué estructura usa cada pestaña
- **PROYECTO_COMPLETADO.txt** — Resumen técnico completo v2.0
- **test_arreglos.py** — 3 tests de validación

---

## 🔗 Entradas Principales

\\\python
# GUI (interfaz gráfica)
from gui import main
main()

# Lógica pura (sin I/O)
from local import Local
local = Local()
local.iniciar_pedido("Ana", "Norte")
local.agregar(101)
local.confirmar()

# Demo automática en consola
python main.py --demo
\\\

---

## 🎉 Estado Actual

- ✅ GUI corriendo sin errores
- ✅ Todos los problemas de v1 solucionados
- ✅ 9 estructuras implementadas
- ✅ 3 tests de validación pasados
- ✅ Documentación completa
- ✅ Listo para explicación final

---

**Versión:** 2.0 | **Estado:** Completado | **Fecha:** Octubre 2026
