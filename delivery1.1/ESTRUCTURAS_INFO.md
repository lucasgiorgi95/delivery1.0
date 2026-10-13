# Estructuras de Datos - Información y Complejidad

Este documento describe todas las estructuras de datos implementadas en el proyecto y su información de complejidad.

## Acceso a la Información

### Interfaz Gráfica
1. Abre la aplicación con `python main.py`
2. Dirígete a la pestaña **"Estructuras"**
3. Selecciona cualquier estructura del dropdown para ver:
   - Descripción
   - Operaciones principales
   - Complejidad (Big O, Theta, Omega)
   - Usos en el local

### Consola
1. Abre la aplicación con `python main.py` (en modo consola)
2. Selecciona opción **9) Ver estructuras**
3. Elige:
   - **1)** Ver todas las estructuras (lista completa)
   - **2)** Ver información detallada de una estructura específica

## Estructuras Implementadas

### 1. **Pila (Stack)**
- **Descripción:** Última entrada, primera salida (LIFO)
- **Operaciones:** apilar, desapilar
- **Complejidad:**
  - Big O: O(1)
  - Theta: Θ(1)
  - Omega: Ω(1)
- **Usos en el local:**
  - Quitar el último producto del pedido
  - Combo por presupuesto (backtracking)
  - Calculadora postfija

### 2. **Cola (Queue)**
- **Descripción:** Primera entrada, primera salida (FIFO)
- **Operaciones:** encolar, desencolar
- **Complejidad:**
  - Big O: O(1)
  - Theta: Θ(1)
  - Omega: Ω(1)
- **Usos en el local:**
  - Pedidos normales en orden de llegada
  - Cola circular: últimos 3 pedidos despachados

### 3. **Cola de Prioridad (Heap)**
- **Descripción:** Estructura de árbol binario para prioridades
- **Operaciones:** insertar, extraer_min
- **Complejidad:**
  - Big O: O(log n)
  - Theta: Θ(log n)
  - Omega: Ω(1) insert, Ω(log n) extract
- **Usos en el local:**
  - Pedidos urgentes: sale primero el más apurado

### 4. **Lista Simple**
- **Descripción:** Nodos enlazados, recorrido en una dirección
- **Operaciones:** insertar, eliminar, recorrer
- **Complejidad:**
  - Big O: O(n) insert_final, O(1) insert_inicio
  - Theta: Θ(n) en promedio
  - Omega: Ω(1)
- **Usos en el local:**
  - Productos de un pedido

### 5. **Lista Doble**
- **Descripción:** Nodos enlazados, recorrido bidireccional
- **Operaciones:** insertar, eliminar, recorrer
- **Complejidad:**
  - Big O: O(n)
  - Theta: Θ(n)
  - Omega: Ω(1)
- **Usos en el local:**
  - Historial de estados del pedido (antes/después)

### 6. **Lista Circular**
- **Descripción:** Nodos enlazados en círculo, recorrido cíclico
- **Operaciones:** insertar, rotar
- **Complejidad:**
  - Big O: O(1) rotar
  - Theta: Θ(1)
  - Omega: Ω(1)
- **Usos en el local:**
  - Turnos rotativos de repartidores

### 7. **Árbol Binario de Búsqueda (ABB)**
- **Descripción:** Árbol donde izq < padre < derecha
- **Operaciones:** buscar, insertar, eliminar
- **Complejidad:**
  - Big O: O(n) peor caso
  - Theta: Θ(log n) promedio
  - Omega: Ω(1) búsqueda lucky
- **Usos en el local:**
  - Catálogo por código

### 8. **Árbol AVL**
- **Descripción:** ABB auto-balanceado con rotaciones
- **Operaciones:** buscar, insertar, eliminar
- **Complejidad:**
  - Big O: O(log n)
  - Theta: Θ(log n)
  - Omega: Ω(1)
- **Usos en el local:**
  - Catálogo por código (mantiene balance)

### 9. **Grafo - Lista de Adyacencia**
- **Descripción:** Estructura para representar conexiones entre zonas
- **Operaciones:** BFS, DFS, búsqueda de ruta
- **Complejidad:**
  - Big O: O(V + E)
  - Theta: Θ(V + E)
  - Omega: Ω(V) best case
- **Usos en el local:**
  - Mapa de zonas de entrega
  - Ruta con menos paradas (BFS)
  - Zonas alcanzables desde el local (DFS)

### 10. **Ordenamiento - Merge Sort**
- **Descripción:** Divide y conquista: divide en mitades, ordena, fusiona
- **Operaciones:** ordenar
- **Complejidad:**
  - Big O: O(n log n)
  - Theta: Θ(n log n)
  - Omega: Ω(n log n)
- **Usos en el local:**
  - Catálogo ordenado por precio

### 11. **Ordenamiento - Bubble Sort**
- **Descripción:** Intercambia adyacentes si están mal ordenados
- **Operaciones:** ordenar
- **Complejidad:**
  - Big O: O(n²)
  - Theta: Θ(n²)
  - Omega: Ω(n) si ya está ordenado
- **Usos en el local:**
  - Comparación de complejidad (menú 8)

### 12. **Ordenamiento - Quick Sort**
- **Descripción:** Divide por pivote, ordena particiones
- **Operaciones:** ordenar
- **Complejidad:**
  - Big O: O(n²) peor caso
  - Theta: Θ(n log n) promedio
  - Omega: Ω(n log n)
- **Usos en el local:**
  - Comparación de complejidad (menú 8)

### 13. **Búsqueda Secuencial**
- **Descripción:** Recorre de inicio a fin hasta encontrar
- **Operaciones:** buscar
- **Complejidad:**
  - Big O: O(n)
  - Theta: Θ(n)
  - Omega: Ω(1) found at start
- **Usos en el local:**
  - Producto por nombre (sin ordenar)

### 14. **Búsqueda Binaria**
- **Descripción:** Divide por la mitad, descarta mitad innecesaria
- **Operaciones:** buscar
- **Complejidad:**
  - Big O: O(log n)
  - Theta: Θ(log n)
  - Omega: Ω(1)
- **Usos en el local:**
  - Producto por precio exacto (catálogo ordenado)

### 15. **Backtracking**
- **Descripción:** Explora todas las combinaciones, retrocede si no funciona
- **Operaciones:** buscar combo
- **Complejidad:**
  - Big O: O(2^n)
  - Theta: Θ(2^n)
  - Omega: Ω(1)
- **Usos en el local:**
  - Combo que suma justo el presupuesto del cliente

### 16. **Notación Postfija**
- **Descripción:** Convierte infija a postfija y evalúa
- **Operaciones:** parsear y evaluar
- **Complejidad:**
  - Big O: O(n)
  - Theta: Θ(n)
  - Omega: Ω(n)
- **Usos en el local:**
  - Calculadora de caja: (5500+3000)*90/100

## Notas sobre Complejidad

- **Big O (O)**: Cota superior - peor caso
- **Theta (Θ)**: Cota exacta - caso promedio
- **Omega (Ω)**: Cota inferior - mejor caso

Cada estructura está optimizada para el contexto específico del local de comidas, balanceando simplicidad, eficiencia y claridad de propósito.
