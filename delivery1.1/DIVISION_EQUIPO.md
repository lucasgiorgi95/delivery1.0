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

---

# 🎤 Speeches para la Exposición

> Estos textos son para estudiar y adaptar con tus propias palabras. No los leas en voz alta, usálos para entender qué decir y cómo decirlo.

---

## 🟦 Speech de Lucas

---

### Nodo

"Bueno, yo arranco con la estructura más básica del proyecto: el **Nodo**.

Un nodo es simplemente un objeto que guarda dos cosas: un **dato** y una **referencia al siguiente nodo**. Eso es todo. Pero es la base de casi todo lo que vamos a ver hoy.

Lo llamamos estructura autorreferenciada porque apunta a algo de su mismo tipo. Es como una cadena: cada eslabón conoce al siguiente.

En nuestro proyecto, el Nodo está en `nodo.py` y tiene dos variantes: el `Nodo` simple, con solo `dato` y `siguiente`, y el `NodoDoble`, que además tiene `anterior`.

Sin el Nodo, no existirían la pila, la cola ni las listas. Cada producto que el cliente agrega a su pedido vive dentro de un nodo. Cada estado del historial —creado, confirmado, despachado— también vive en un nodo doble."

---

### Lista Simple

"La **Lista Simple** es una cadena de nodos donde cada uno apunta al siguiente, pero no al anterior.

La característica más importante es que solo guardamos la **cabeza**, el primer nodo. Entonces insertar al inicio es O(1), lo hago directo. Pero insertar al final es O(n) porque tengo que recorrer toda la cadena hasta llegar al último.

También puedo eliminar cualquier elemento si conozco una condición, sin necesidad de saber su posición exacta.

En el proyecto, la `ListaSimple` guarda los **productos de cada pedido** en el orden en que se cargaron. Cuando el cliente agrega una pizza y después una gaseosa, esas dos van quedando encadenadas en la lista. Si vas al código de `modelos.py`, en la clase `Pedido`, el atributo `items` es una `ListaSimple`.

También aparece dentro del Grafo: cada zona guarda sus vecinos en una `ListaSimple`."

---

### Árbol AVL

"El **AVL** es la estructura más compleja que me tocó, y también la más interesante.

Primero hay que entender el ABB: un árbol donde cada nodo tiene a su izquierda claves menores y a su derecha claves mayores. Buscar en un ABB es muy rápido, O(log n)... pero solo si el árbol está balanceado. Si inserto los productos en orden —101, 102, 103...— el árbol se convierte en una lista larga y buscar vuelve a ser O(n).

Ahí entra el AVL. El AVL es un ABB que **se balancea solo** después de cada inserción o eliminación. Lo hace con **rotaciones**: si un subárbol queda demasiado alto, lo rota para equilibrarlo. Garantiza que la diferencia de altura entre ramas nunca supera 1.

En el proyecto, el **catálogo de productos** vive en un AVL ordenado por código. La pestaña 'Catálogo' de la interfaz muestra todos los productos recorriendo el árbol en **inorden**, que devuelve los nodos de menor a mayor código. Y como es AVL, aunque cargues los productos en orden, las búsquedas siguen siendo O(log n) siempre."

---
---

## 🟧 Speech de Axel

---

### Pila

"A mí me tocó la **Pila**, que es una estructura LIFO: Last In, First Out. El último en entrar es el primero en salir. Como una pila de platos: siempre agarrás del tope.

Las operaciones son tres: **apilar** para agregar, **desapilar** para sacar, y **ver tope** para mirar sin sacar. Las tres son O(1), rapidísimas.

Implementamos dos versiones: la `PilaEstatica`, con un arreglo de tamaño fijo, y la `PilaDinamica`, con nodos enlazados sin límite de tamaño.

En el proyecto, la pila implementa el botón **'Quitar último'** del panel de pedidos. Cada vez que el cliente agrega un producto, ese producto se guarda en la lista del pedido pero también se **apila** en `_cargados`. Si el cliente se arrepiente del último ítem, hacemos `desapilar()` y lo eliminamos. Es el clásico 'deshacer'.

La pila también aparece en el DFS del grafo: el recorrido en profundidad usa una pila para saber por dónde continuar."

---

### Lista Doble y Circular

"Me tocaron dos listas con características especiales.

La **Lista Doble**: a diferencia de la simple, cada nodo apunta al siguiente **y al anterior**. Además guardamos puntero a la cabeza y a la cola. Eso nos permite insertar y eliminar en cualquiera de los dos extremos en O(1), y también recorrer la lista de atrás para adelante.

En el proyecto, la `ListaDoble` guarda el **historial de estados de cada pedido**. Cuando un pedido pasa de 'creado' a 'confirmado' a 'despachado', cada estado se registra al final. Y al tener puntero hacia atrás, podríamos ver el historial en reversa si lo necesitáramos.

La **Lista Circular**: el último nodo apunta de vuelta al primero. No tiene fin. Solo guardamos referencia al último nodo, y el primero es `ultimo.siguiente`.

En el proyecto se usa para los **turnos rotativos de repartidores**. Imaginá que tenés tres repartidores: Ana, Juan, Pedro. Al despachar un pedido, el sistema rota al siguiente con `siguiente_turno()`. Cuando llega al final de la lista, vuelve a empezar por Ana automáticamente."

---

### Grafo con BFS y DFS

"El **Grafo** es la estructura más compleja que me tocó. Representa conexiones entre elementos, no una secuencia lineal como las listas.

Un grafo tiene **vértices** —los puntos— y **aristas** —las conexiones. Implementamos dos formas de guardarlo:
- **Matriz de adyacencia**: una tabla donde `matriz[i][j] = 1` si hay conexión. Consultar si dos zonas están unidas es O(1), pero ocupa O(V²) de memoria.
- **Lista de adyacencia**: cada zona guarda solo la lista de sus vecinos. Ocupa O(V+A), mucho mejor cuando hay pocas conexiones.

En el proyecto usamos la `GrafoLista` porque el mapa de zonas —Local, Norte, Sur, Costanera, Isla— tiene pocas conexiones.

Para recorrer el grafo tenemos dos algoritmos:
- **BFS** usa una **cola**: visita primero todos los vecinos directos, luego los vecinos de los vecinos. Sirve para encontrar la ruta con **menos paradas**.
- **DFS** usa una **pila**: sigue un camino hasta el fondo y vuelve atrás. Sirve para saber **todas las zonas alcanzables**.

En la pestaña 'Zonas' de la GUI podés escribir una zona destino y el BFS te dice el camino más corto desde el local."

---
---

## 🟩 Speech de Enrique

---

### Cola

"Yo empiezo con la **Cola**, que es la estructura más natural del mundo: FIFO, First In, First Out. El primero en llegar es el primero en ser atendido. Como la cola de un banco.

Las operaciones son **encolar** para agregar al final, **desencolar** para sacar del frente, y **ver frente** para mirar sin sacar. Todas O(1).

Implementamos dos versiones:
- `ColaSimple`: usa nodos enlazados con puntero al frente y al final.
- `ColaCircular`: usa un arreglo fijo donde los índices dan la vuelta con el operador módulo (%). Cuando llegas al final del arreglo, volvés al principio.

En el proyecto, la `ColaSimple` gestiona los **pedidos normales en espera**. Cuando un cliente confirma su pedido, entra a la cola. El repartidor despacha siempre al primero que llegó, que es lo justo.

La `ColaCircular` implementa la **pizarra de 'últimos 3 despachados'** en la interfaz. Tiene capacidad 3. Al despachar el cuarto pedido, el más antiguo se sobreescribe automáticamente. El módulo se encarga de que el índice no se pase del tamaño."

---

### Cola de Prioridad

"La **Cola de Prioridad** es una cola con un twist: no sale el que llegó primero, sino el que tiene **mayor prioridad**.

Se implementa con un **heap binario mínimo**, que es un árbol binario completo guardado en un arreglo. La regla es que el padre siempre es menor que sus hijos. Así, la raíz —posición 0 del arreglo— siempre es el elemento más urgente.

Para encolar, agrego al final y 'subo' el elemento comparándolo con su padre hasta que quede en su lugar. Para desencolar, saco la raíz, pongo el último elemento arriba y lo 'bajo' comparándolo con sus hijos. Ambas operaciones son O(log n).

En el proyecto maneja la **cola de despacho con urgentes**. Los pedidos urgentes entran con prioridad 0, los normales con prioridad 1. El botón 'Despachar siguiente' siempre saca al más urgente. Y si hay dos urgentes, sale primero el que llegó antes porque guardamos el orden de llegada como desempate."

---

### Árbol ABB

"El **ABB**, Árbol Binario de Búsqueda, es la base de los árboles en este proyecto.

La regla es simple: para cada nodo, todo lo que está a la **izquierda** tiene clave menor, y todo lo que está a la **derecha** tiene clave mayor. Eso nos permite buscar de forma muy eficiente: en cada paso descartamos la mitad del árbol. Es O(log n) si el árbol está balanceado.

Las operaciones más interesantes son insertar y eliminar, que son recursivas. El caso más difícil de la eliminación es cuando el nodo tiene **dos hijos**: no podés simplemente borrarlo. Lo que hacés es encontrar el **sucesor inorden** —el nodo más pequeño del subárbol derecho— copiar su clave al nodo que querés borrar, y eliminar el sucesor.

En el proyecto, el ABB es la base sobre la que construimos el AVL. El recorrido **inorden** del ABB devuelve todos los productos ordenados de menor a mayor código, que es lo que muestra la pestaña 'Catálogo'. Los recorridos preorden y postorden también están implementados y se pueden ver en la pestaña 'Estructuras' de la GUI."

---
