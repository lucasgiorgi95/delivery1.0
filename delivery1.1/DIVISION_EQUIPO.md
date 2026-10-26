# 👥 División de Estructuras — Equipo

**Proyecto:** Sistema de Pedidos - Local de Comidas v2.0  
**Materia:** Estructura de Datos  

---

## 🟦 Lucas

### 🟢 Fácil — Nodo (`estructuras/nodo.py`)

**Concepto:**  
Es la unidad mínima de todas las estructuras dinámicas. Un nodo guarda un dato y una referencia (puntero) al siguiente nodo del mismo tipo. Es una estructura autorreferenciada: apunta a algo de su mismo tipo.

**En el proyecto:**  
Es la base de todo. Sin el `Nodo`, no existirían la pila, la cola ni las listas enlazadas. Cada producto que se agrega a un pedido vive dentro de un nodo de la `ListaSimple`. Cada estado del historial del pedido vive en un `NodoDoble`.

---

### 🟡 Media — Lista Simple (`estructuras/listas.py` → `ListaSimple`)

**Concepto:**  
Cada nodo apunta solo al siguiente. Para insertar al final hay que recorrer toda la lista (O(n)), pero insertar al inicio es O(1). Permite eliminar elementos que cumplan una condición sin saber su posición exacta.

**En el proyecto:**  
Guarda los **productos de cada pedido** en el orden en que fueron cargados. Cuando el cliente agrega una hamburguesa y luego una bebida, ambas quedan en una `ListaSimple` dentro del `Pedido`. También se usa internamente en el grafo de zonas (`GrafoLista`) para guardar los vecinos de cada zona.

---

### 🔴 Difícil — Árbol AVL (`estructuras/arbol.py` → `AVL`)

**Concepto:**  
Es un Árbol Binario de Búsqueda que se **autobalancea** con rotaciones. Mantiene la diferencia de altura entre subárboles en máximo 1, garantizando que buscar, insertar y eliminar siempre cuestan O(log n), sin importar el orden de inserción.

**En el proyecto:**  
El **catálogo de productos** se guarda en un AVL ordenado por código. Gracias al balanceo automático, aunque los productos se carguen en orden (101, 102, 103...), el árbol no degenera en una lista y las búsquedas siguen siendo rápidas. La pestaña "Catálogo" de la GUI muestra todos los productos recorriéndolo en inorden (de menor a mayor código).

---
---

## 🟧 Axel

### 🟢 Fácil — Pila (`estructuras/pila.py`)

**Concepto:**  
Estructura LIFO (Last In, First Out): el último en entrar es el primero en salir. Las operaciones apilar y desapilar son O(1). Hay dos implementaciones: con arreglo de tamaño fijo (`PilaEstatica`) y con nodos enlazados (`PilaDinamica`).

**En el proyecto:**  
Implementa el botón **"Quitar último"** del panel de armado de pedidos. Cada vez que se agrega un producto al pedido, también se apila en `_cargados` (una `PilaDinamica` dentro de `Pedido`). Si el cliente se arrepiente del último ítem, se desapila y se elimina de la lista. También se usa en el algoritmo DFS del grafo de zonas.

---

### 🟡 Media — Lista Doble y Circular (`estructuras/listas.py` → `ListaDoble`, `ListaCircular`)

**Concepto:**  
- **Lista Doble:** cada nodo apunta al anterior y al siguiente. Se puede recorrer en ambas direcciones e insertar/eliminar en cualquier extremo en O(1).  
- **Lista Circular:** el último nodo apunta de vuelta al primero. Ideal para turnos rotativos: nunca tiene fin.

**En el proyecto:**  
- La `ListaDoble` guarda el **historial de estados** de cada pedido (ej: "creado → confirmado → despachado"). Al tener puntero hacia atrás, se podría recorrer el historial en orden inverso.  
- La `ListaCircular` maneja los **turnos rotativos de repartidores**: cada vez que se despacha un pedido, el sistema puede rotar al siguiente repartidor disponible de forma cíclica.

---

### 🔴 Difícil — Grafo con BFS y DFS (`estructuras/grafo.py`)

**Concepto:**  
Un grafo es un conjunto de vértices conectados por aristas. Se puede representar con una **matriz de adyacencia** (O(V²) memoria, consulta O(1)) o con una **lista de adyacencia** (O(V+A) memoria, mejor para grafos dispersos). BFS recorre por niveles usando una cola; DFS recorre en profundidad usando una pila.

**En el proyecto:**  
Modela el **mapa de zonas de delivery** (Local, Norte, Sur, Costanera, Isla). Se usa `GrafoLista` porque las conexiones son pocas. La pestaña "Zonas" de la GUI permite:  
- **BFS** → encontrar la ruta con **menos paradas** hasta una zona (ej: la más corta para llegar a Isla).  
- **DFS** → descubrir **todas las zonas alcanzables** desde el local.

---
---

## 🟩 Enrique

### 🟢 Fácil — Cola (`estructuras/cola.py`)

**Concepto:**  
Estructura FIFO (First In, First Out): el primero en entrar es el primero en salir. `ColaSimple` usa nodos enlazados con puntero al frente y al final, haciendo encolar y desencolar O(1). `ColaCircular` usa un arreglo de tamaño fijo donde los índices dan la vuelta con módulo (%).

**En el proyecto:**  
- La `ColaSimple` gestiona los **pedidos normales en espera**: el primero en confirmar es el primero en despacharse (orden justo).  
- La `ColaCircular` implementa la **pizarra de "últimos 3 despachados"** en la GUI: al encolar el cuarto, el más viejo se sobreescribe automáticamente gracias al arreglo circular.

---

### 🟡 Media — Cola de Prioridad (`estructuras/cola_prioridad.py`)

**Concepto:**  
Cola que despacha primero al elemento con **mayor prioridad** (menor número). Se implementa con un heap binario mínimo guardado en un arreglo: el hijo izquierdo de `i` está en `2i+1`, el derecho en `2i+2`. Encolar y desencolar son O(log n). Ante igual prioridad, sale primero el que llegó antes.

**En el proyecto:**  
Maneja la **cola de pedidos urgentes**. Cuando un pedido se marca como urgente, entra con prioridad 0; los normales entran con prioridad 1. El botón "Despachar siguiente" siempre saca al pedido más urgente primero, y entre urgentes respeta el orden de llegada. Es la estructura central del panel de despacho.

---

### 🔴 Difícil — Árbol ABB (`estructuras/arbol.py` → `ABB`)

**Concepto:**  
Árbol Binario de Búsqueda: para cada nodo, todas las claves del subárbol izquierdo son menores y las del derecho son mayores. Buscar, insertar y eliminar cuestan O(log n) si está balanceado, pero pueden degradarse a O(n) si se insertan claves en orden. La eliminación con dos hijos requiere encontrar el **sucesor inorden** (el menor del subárbol derecho).

**En el proyecto:**  
Es la base del `AVL`. El ABB puro se usa para entender la lógica de búsqueda ordenada por código de producto. La búsqueda binaria de la pestaña "Búsquedas" (buscar producto por precio exacto en O(log n)) se apoya en la propiedad de orden del ABB. Los recorridos **inorden, preorden y postorden** están implementados y se pueden visualizar en la pestaña "Estructuras".

---

## 📊 Resumen

| Persona | 🟢 Fácil | 🟡 Media | 🔴 Difícil |
|---------|----------|----------|------------|
| **Lucas** | Nodo | Lista Simple | Árbol AVL |
| **Axel** | Pila | Lista Doble/Circular | Grafo (BFS/DFS) |
| **Enrique** | Cola | Cola de Prioridad | Árbol ABB |

> Cada uno debe poder explicar sus tres estructuras: cómo funcionan internamente y dónde aparecen en el proyecto.
