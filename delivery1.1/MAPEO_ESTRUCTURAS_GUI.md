# Mapeo: Estructuras y Algoritmos en la GUI

## 📍 Dónde se Usa Cada Estructura/Algoritmo en la Interfaz

---

## 🏗️ ESTRUCTURAS DE DATOS

### 1. **PILA (Stack)** - LIFO

#### 📍 Ubicación en la GUI
**Panel Izquierdo → Botón "🗑️ QUITAR"**

#### 🎯 Cómo se usa
1. Agregá productos a un pedido
2. Click en "🗑️ QUITAR"
3. Se elimina el **último producto agregado** (LIFO)

#### 💻 Implementación
```python
# Cuando agregás:
pedido._cargados.apilar(producto)

# Cuando quitás:
producto = pedido._cargados.desapilar()  # ← PILA
```

#### ✅ Cómo demostrarlo
```
1. Cliente: "Ana"
2. Agregar: 101 (Hamburguesa)
3. Agregar: 103 (Papas)
4. Agregar: 104 (Gaseosa)
5. Click "🗑️ QUITAR" → Sale 104 (último)
6. Click "🗑️ QUITAR" → Sale 103 (penúltimo)
```

---

### 2. **COLA SIMPLE (Queue)** - FIFO

#### 📍 Ubicación en la GUI
**Panel Izquierdo → "📋 PEDIDOS EN ESPERA" (pedidos normales)**

#### 🎯 Cómo se usa
1. Creá pedidos **sin marcar urgente** (⚪)
2. Se encolan en orden de llegada
3. Al despachar, sale el **primero que llegó** (FIFO)

#### 💻 Implementación
```python
# Cuando confirmás pedido normal:
self.local.normales.encolar(pedido)  # ← COLA SIMPLE

# Cuando despachás:
pedido = self.local.normales.desencolar()  # ← FIFO
```

#### ✅ Cómo demostrarlo
```
1. Crear pedido: Ana (sin urgente) ⚪
2. Crear pedido: Beto (sin urgente) ⚪
3. Crear pedido: Cami (sin urgente) ⚪
4. Lista muestra: Ana → Beto → Cami
5. Click "📦 DESPACHAR" → Sale Ana (primero)
6. Click "📦 DESPACHAR" → Sale Beto (segundo)
```

---

### 3. **COLA DE PRIORIDAD (Heap)** - Priority Queue

#### 📍 Ubicación en la GUI
**Panel Izquierdo → "📋 PEDIDOS EN ESPERA" (pedidos urgentes 🔴)**

#### 🎯 Cómo se usa
1. Creá pedidos **marcando "🔴 Es URGENTE"**
2. Ajustá minutos promesa (10, 15, 20)
3. Los urgentes salen **primero** (menor minutos primero)

#### 💻 Implementación
```python
# Cuando confirmás pedido urgente:
self.local.urgentes.encolar(pedido, minutos)  # ← HEAP (min-heap)

# Cuando despachás:
pedido = self.local.urgentes.desencolar()  # ← Menor prioridad primero
```

#### ✅ Cómo demostrarlo
```
1. Crear: Ana (normal) ⚪
2. Crear: Beto (urgente, 20 min) 🔴
3. Crear: Cami (urgente, 10 min) 🔴
4. Lista muestra: Cami (10min) → Beto (20min) → Ana
5. Click "📦 DESPACHAR" → Sale Cami (más urgente)
6. Click "📦 DESPACHAR" → Sale Beto (siguiente urgente)
7. Click "📦 DESPACHAR" → Sale Ana (normal)
```

---

### 4. **COLA CIRCULAR** - Circular Queue

#### 📍 Ubicación en la GUI
**Panel Izquierdo → "✅ ÚLTIMOS DESPACHADOS"**

#### 🎯 Cómo se usa
1. Despachá 5+ pedidos
2. Solo se muestran los **últimos 3**
3. Al agregar el 4º, se borra el 1º (circular)

#### 💻 Implementación
```python
# Cola circular con capacidad 3:
self.local.listos = ColaCircular(3)

# Al despachar:
if self.local.listos.esta_llena():
    self.local.listos.desencolar()  # ← Borra el más viejo
self.local.listos.encolar(pedido)  # ← Agrega el nuevo
```

#### ✅ Cómo demostrarlo
```
1. Click "📊 DEMO" (carga 4 pedidos ya despachados)
2. Sección "ÚLTIMOS DESPACHADOS" muestra solo 3
3. Pestaña "📈 Estadísticas":
   - "En pizarra: 3" ← Cola circular
   - "Total despachados: 4" ← Contador real
```

---

### 5. **LISTA SIMPLE** - Singly Linked List

#### 📍 Ubicación en la GUI
**Panel Izquierdo → "📦 PRODUCTOS CARGADOS"**

#### 🎯 Cómo se usa
1. Los productos de un pedido se guardan en lista simple
2. Se recorre para mostrar y calcular total

#### 💻 Implementación
```python
# Los productos del pedido:
pedido.items = ListaSimple()

# Al agregar:
pedido.items.insertar_final(producto)  # ← LISTA SIMPLE

# Al mostrar:
for producto in pedido.items:  # ← Recorrido
    print(producto)
```

#### ✅ Cómo demostrarlo
```
1. Agregá 3 productos al pedido
2. Sección "PRODUCTOS CARGADOS" los muestra en orden
3. Se calcula el TOTAL sumando todos
```

---

### 6. **LISTA DOBLE** - Doubly Linked List

#### 📍 Ubicación en la GUI
**Interno (historial del pedido, no visible directamente)**

#### 🎯 Cómo se usa
Cada pedido tiene historial de estados que puede recorrerse adelante/atrás:
- "Confirmado"
- "Despachado"

#### 💻 Implementación
```python
# Historial del pedido:
pedido.historial = ListaDoble()

# Agregar estado:
pedido.registrar("Confirmado")  # ← LISTA DOBLE
pedido.registrar("Despachado")

# Recorrer normal o inverso:
for estado in pedido.historial:
    print(estado)
for estado in pedido.historial.iter_inverso():  # ← Bidireccional
    print(estado)
```

#### ✅ Cómo demostrarlo (desde consola Python)
```python
from local import Local
l = Local()
l.iniciar_pedido("Test", "Norte")
l.agregar(101)
p = l.confirmar()
l.despachar()
print(list(p.historial))  # ['Confirmado', 'Despachado']
print(list(p.historial.iter_inverso()))  # ['Despachado', 'Confirmado']
```

---

### 7. **LISTA CIRCULAR** - Circular Linked List

#### 📍 Ubicación en la GUI
**Interno (repartidores rotativos)**

#### 🎯 Cómo se usa
Los repartidores rotan automáticamente:
- Ana → María → Juan → Ana → María...

#### 💻 Implementación
```python
# Repartidores:
self.local.repartidores = ListaCircular()
# ["Ana", "María", "Juan"]

# Al despachar:
repartidor = self.local.repartidores.siguiente_turno()  # ← LISTA CIRCULAR (rota)
```

#### ✅ Cómo demostrarlo
```
1. Creá 3 pedidos con zona (no retiro)
2. Despachá los 3
3. Sección "ÚLTIMOS DESPACHADOS" muestra:
   - #1 → Ana
   - #2 → María
   - #3 → Juan
4. Creá otro pedido y despachalo
5. Le toca: Ana (volvió al inicio, circular)
```

---

### 8. **ÁRBOL BINARIO DE BÚSQUEDA (ABB)** - BST

#### 📍 Ubicación en la GUI
**Pestaña "📋 Catálogo"**

#### 🎯 Cómo se usa
Los productos están ordenados por **código** en un ABB.

#### 💻 Implementación
```python
# Catálogo:
self.local.catalogo = ArbolAVL()  # ← Implementa ABB con balanceo

# Buscar por código:
producto = self.local.catalogo.buscar(101)  # ← O(log n)
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "📋 Catálogo"
2. Productos mostrados en orden de código (inorden):
   101, 102, 103, 104, 105, 106, 107
3. Pestaña "📈 Estadísticas" → "Árbol AVL":
   - Altura: 3
   - Nodos: 7
```

---

### 9. **ÁRBOL AVL** - Self-Balancing BST

#### 📍 Ubicación en la GUI
**Pestaña "📋 Catálogo" + "📈 Estadísticas"**

#### 🎯 Cómo se usa
Mismo que ABB pero **auto-balanceado** con rotaciones.

#### 💻 Implementación
```python
# AVL mantiene balance:
self.local.catalogo = ArbolAVL()

# Insertar hace rotaciones automáticas:
catalogo.insertar(codigo, producto)  # ← Rotaciones si desbalanceado
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "📈 Estadísticas"
2. "Árbol AVL":
   - Altura: 3 (balanceado)
   - Si fuera ABB desbalanceado: altura 7
3. Recorrido inorden = orden por código
```

---

### 10. **GRAFO (Lista de Adyacencia)** - Graph

#### 📍 Ubicación en la GUI
**Pestaña "🗺️ Zonas"**

#### 🎯 Cómo se usa
Mapa de zonas de entrega con rutas:
```
Local → Centro → Norte
       ↓
       Sur → Costanera
```

#### 💻 Implementación
```python
# Grafo con lista de adyacencia:
self.local.zonas = Grafo()
# Local → [Centro]
# Centro → [Norte, Sur]
# Sur → [Costanera]
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "🗺️ Zonas"
2. Muestra:
   - Zonas alcanzables: Centro, Norte, Sur, Costanera
   - Recorrido BFS: Local → Centro → Norte → Sur → Costanera
   - Rutas más cortas:
     • Centro: Local → Centro
     • Norte: Local → Centro → Norte
     • Sur: Local → Centro → Sur
     • Costanera: Local → Centro → Sur → Costanera
```

---

## 🔍 ALGORITMOS DE BÚSQUEDA

### 11. **BÚSQUEDA BINARIA** - Binary Search O(log n)

#### 📍 Ubicación en la GUI
**Pestaña "🔍 Búsquedas" → Por PRECIO EXACTO**

#### 🎯 Cómo se usa
1. Abre dropdown de precios
2. Selecciona un precio (ej: 3000)
3. Click "Buscar"
4. Resultado: producto con ese precio exacto

#### 💻 Implementación
```python
# Productos ordenados por precio (merge sort):
productos_ordenados = self.local.productos_por_precio()

# Búsqueda binaria:
producto = busqueda_binaria(productos_ordenados, precio)  # ← O(log n)
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "🔍 Búsquedas"
2. Precio: [Selecciona "3000"]
3. Click "Buscar"
4. Resultado: ✅ 103 - Papas fritas ($3000)
```

---

### 12. **BÚSQUEDA SECUENCIAL** - Linear Search O(n)

#### 📍 Ubicación en la GUI
**Pestaña "🔍 Búsquedas" → Por NOMBRE**

#### 🎯 Cómo se usa
1. Abre dropdown de nombres
2. Selecciona un producto (ej: "Hamburguesa simple")
3. Click "Buscar"
4. Recorre todos los productos hasta encontrarlo

#### 💻 Implementación
```python
# Búsqueda secuencial (no ordenado por nombre):
def buscar_por_nombre(nombre):
    for producto in productos:  # ← O(n)
        if producto.nombre == nombre:
            return producto
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "🔍 Búsquedas"
2. Nombre: [Selecciona "Hamburguesa simple"]
3. Click "Buscar"
4. Resultado: ✅ 101 - Hamburguesa simple ($5500)
```

---

### 13. **BACKTRACKING** - O(2^n)

#### 📍 Ubicación en la GUI
**Pestaña "🔍 Búsquedas" → COMBO por PRESUPUESTO**

#### 🎯 Cómo se usa
1. Ingresa presupuesto (spinbox): ej 13000
2. Click "Buscar"
3. Encuentra combinación de productos que suma **exactamente** ese valor

#### 💻 Implementación
```python
# Backtracking recursivo:
def combo(productos, presupuesto, actual=[]):
    if sum(actual) == presupuesto:
        return actual  # ← Solución
    if sum(actual) > presupuesto:
        return None  # ← Poda
    for p in productos:
        resultado = combo(productos, presupuesto, actual + [p])  # ← Recursión
        if resultado:
            return resultado
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "🔍 Búsquedas"
2. Presupuesto: [13000]
3. Click "Buscar"
4. Resultado: ✅ Hamburguesa simple + Hamburguesa doble = $13000
```

---

## 📊 ALGORITMOS DE ORDENAMIENTO

### 14. **MERGE SORT** - O(n log n)

#### 📍 Ubicación en la GUI
**Pestaña "📋 Catálogo" (implícito cuando se ordena por precio)**

#### 🎯 Cómo se usa
Los productos se ordenan por precio usando merge sort.

#### 💻 Implementación
```python
# Ordenar productos por precio:
productos_ordenados = merge_sort(productos, key=lambda p: p.precio)  # ← O(n log n)
```

#### ✅ Cómo demostrarlo
```
1. Ver productos ordenados por precio (de menor a mayor):
   - Gaseosa: $2000
   - Helado: $2500
   - Papas: $3000
   - Cerveza: $3500
   - Hamburguesa simple: $5500
   - Hamburguesa doble: $7500
   - Pizza: $8000
```

---

### 15. **BFS (Breadth-First Search)** - O(V + E)

#### 📍 Ubicación en la GUI
**Pestaña "🗺️ Zonas" → Recorrido BFS**

#### 🎯 Cómo se usa
Encuentra rutas con **menos paradas** desde el Local.

#### 💻 Implementación
```python
# BFS en grafo:
def bfs(inicio):
    cola = Cola()
    cola.encolar(inicio)
    visitados = set()
    
    while not cola.esta_vacia():
        actual = cola.desencolar()
        visitados.add(actual)
        for vecino in grafo[actual]:
            if vecino not in visitados:
                cola.encolar(vecino)  # ← FIFO = nivel por nivel
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "🗺️ Zonas"
2. "Recorrido BFS: Local → Centro → Norte → Sur → Costanera"
3. Orden por niveles:
   - Nivel 0: Local
   - Nivel 1: Centro
   - Nivel 2: Norte, Sur
   - Nivel 3: Costanera
```

---

### 16. **DFS (Depth-First Search)** - O(V + E)

#### 📍 Ubicación en la GUI
**Pestaña "🗺️ Zonas" → Zonas alcanzables**

#### 🎯 Cómo se usa
Encuentra **todas las zonas** alcanzables desde el Local.

#### 💻 Implementación
```python
# DFS en grafo:
def dfs(nodo, visitados):
    visitados.add(nodo)
    for vecino in grafo[nodo]:
        if vecino not in visitados:
            dfs(vecino, visitados)  # ← Recursión = profundidad primero
    return visitados
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "🗺️ Zonas"
2. "Zonas alcanzables: Centro, Norte, Sur, Costanera"
3. Si existiera "Isla" sin conexión, NO aparecería
```

---

## 🧮 ALGORITMOS ESPECIALES

### 17. **NOTACIÓN POSTFIJA (Stack-based Evaluation)** - O(n)

#### 📍 Ubicación en la GUI
**Pestaña "🧮 Calculadora"**

#### 🎯 Cómo se usa
1. Ingresa expresión: `(5500 + 3000) * 90 / 100`
2. Click "Calcular"
3. Convierte a postfija y evalúa con pila

#### 💻 Implementación
```python
# Infija → Postfija:
"(5500 + 3000) * 90 / 100"  →  "5500 3000 + 90 * 100 /"

# Evaluar con pila:
pila = Pila()
for token in postfija:
    if es_numero(token):
        pila.apilar(token)
    else:  # operador
        b = pila.desapilar()
        a = pila.desapilar()
        resultado = operar(a, token, b)
        pila.apilar(resultado)
return pila.desapilar()  # ← Resultado final
```

#### ✅ Cómo demostrarlo
```
1. Pestaña "🧮 Calculadora"
2. Expresión: (5500 + 3000) * 90 / 100
3. Click "Calcular"
4. Resultado: $7,650
```

---

## 📋 TABLA RESUMEN

| Estructura/Algoritmo | Ubicación en GUI | Acción para Verlo |
|---------------------|------------------|-------------------|
| **Pila** | Panel izq → Quitar | Agregar 3 productos, click "🗑️ QUITAR" |
| **Cola Simple** | Panel izq → Pedidos Espera | Crear 3 pedidos normales (⚪) |
| **Cola Prioridad** | Panel izq → Pedidos Espera | Crear 2 urgentes (🔴) con distintos minutos |
| **Cola Circular** | Panel izq → Últimos Despachados | Despachar 5+ pedidos, muestra solo 3 |
| **Lista Simple** | Panel izq → Productos Cargados | Agregar 3 productos a un pedido |
| **Lista Doble** | Interno (historial) | No visible directamente (bidireccional) |
| **Lista Circular** | Interno (repartidores) | Despachar 4+ pedidos, repartidores rotan |
| **ABB/AVL** | Pestaña Catálogo | Ver productos ordenados por código |
| **Grafo** | Pestaña Zonas | Ver mapa de rutas |
| **Búsqueda Binaria** | Pestaña Búsquedas → Precio | Buscar por precio exacto |
| **Búsqueda Secuencial** | Pestaña Búsquedas → Nombre | Buscar por nombre |
| **Backtracking** | Pestaña Búsquedas → Combo | Buscar combo por presupuesto |
| **Merge Sort** | Pestaña Catálogo | Productos ordenados por precio |
| **BFS** | Pestaña Zonas | Recorrido por niveles |
| **DFS** | Pestaña Zonas | Zonas alcanzables |
| **Postfija** | Pestaña Calculadora | Evaluar expresión matemática |

---

## 🎯 DEMO COMPLETA

Para ver **TODAS** las estructuras en acción:

1. **Click "📊 DEMO"** (carga 4 pedidos automáticamente)
2. **Pestaña "🔍 Búsquedas"**:
   - Buscar precio 3000 (binaria)
   - Buscar nombre "Hamburguesa simple" (secuencial)
   - Combo por presupuesto 13000 (backtracking)
3. **Pestaña "🧮 Calculadora"**:
   - Calcular: `(5500 + 3000) * 90 / 100` (postfija)
4. **Pestaña "🗺️ Zonas"**:
   - Ver BFS y DFS
5. **Pestaña "📈 Estadísticas"**:
   - Total despachados vs pizarra
   - Altura del AVL
6. **Pestaña "⚙️ Estructuras"**:
   - Seleccionar cualquiera → Ver O, Θ, Ω

---

**¡Ahora sabés exactamente dónde encontrar cada estructura/algoritmo en la interfaz!** 🎉
