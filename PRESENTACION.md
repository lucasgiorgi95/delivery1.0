# Presentación — Sistema de Pedidos v2.0
### Estructura de Datos · Local de Comidas

---

## SLIDE 1 — Portada

**Sistema de Pedidos — Local de Comidas v2.0**

Materia: Estructura de Datos

Integrantes: Lucas · Axel · Enrique

---

## SLIDE 2 — ¿Qué construimos?

Un sistema de gestión de delivery completo desarrollado en **Python + tkinter**.

**Funcionalidades:**
- Crear pedidos con productos y combos
- Gestionar cola de despacho (normal y urgente)
- Catálogo de productos con búsqueda rápida
- Mapa de zonas con rutas de delivery
- Turnos rotativos de repartidores

**Todas las funcionalidades están soportadas por estructuras de datos implementadas desde cero.**

---

## SLIDE 3 — Arquitectura del proyecto

```
delivery1.0/
├── main.py
├── modelos.py
├── estructuras/
│   ├── nodo.py
│   ├── nodo_arbol.py
│   ├── lista_simple.py
│   ├── lista_doble.py
│   ├── lista_circular.py
│   ├── pila_estatica.py
│   ├── pila_dinamica.py
│   ├── cola_simple.py
│   ├── cola_circular.py
│   ├── cola_prioridad.py
│   ├── abb.py
│   ├── avl.py
│   └── grafo.py
└── gui/
    ├── panel_pedidos.py
    ├── panel_despacho.py
    ├── panel_catalogo.py
    ├── panel_zonas.py
    └── panel_repartidores.py
```

---

## SLIDE 4 — LUCAS · Nodo

**¿Qué es?**
La unidad mínima de todas las estructuras dinámicas.
Guarda un dato y una referencia al siguiente nodo — es **autorreferenciada**.

**¿Qué resuelve en el proyecto?**
Sin el Nodo no existirían la pila, la cola ni las listas.
Cada producto de un pedido vive dentro de un `Nodo`.
Cada estado del historial vive en un `NodoDoble`.

**Archivo:** `estructuras/nodo.py`

```python
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None   # puntero al siguiente nodo


class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None   # puntero hacia adelante
        self.anterior = None    # puntero hacia atrás
```

---

## SLIDE 5 — LUCAS · Lista Simple

**¿Qué es?**
Cadena de nodos donde cada uno apunta solo al siguiente.
- Insertar al inicio: **O(1)**
- Insertar al final: **O(n)** (hay que recorrer hasta el último)

**¿Qué resuelve en el proyecto?**
Guarda los **productos de cada pedido** en el orden en que se agregan.
También la usa el Grafo internamente para guardar los vecinos de cada zona.

**Archivo:** `estructuras/lista_simple.py`

```python
def insertar_final(self, dato):
    nuevo = Nodo(dato)
    if self.esta_vacia():
        self.cabeza = nuevo
        return
    actual = self.cabeza
    while actual.siguiente:       # recorrer hasta el último
        actual = actual.siguiente
    actual.siguiente = nuevo      # enlazar al final

def eliminar_por_condicion(self, condicion):
    # elimina el primer nodo que cumpla la condición
    actual = self.cabeza
    while actual.siguiente:
        if condicion(actual.siguiente.dato):
            actual.siguiente = actual.siguiente.siguiente
            return True
        actual = actual.siguiente
    return False
```

---

## SLIDE 6 — LUCAS · Árbol AVL

**¿Qué es?**
Un Árbol Binario de Búsqueda que **se balancea solo** con rotaciones.
Garantiza O(log n) para buscar, insertar y eliminar **siempre**,
sin importar el orden de inserción.

**Factor de balance** = altura(izq) − altura(der) → debe mantenerse en {-1, 0, 1}

**¿Qué resuelve en el proyecto?**
El **catálogo de productos** vive en un AVL ordenado por código.
La pestaña "Catálogo" recorre el árbol en inorden → muestra productos de menor a mayor código.

**Archivo:** `estructuras/avl.py`

```python
def rotacion_der(self, y):
    #      y              x
    #     / \            / \
    #    x   T3   →    T1   y
    #   / \                / \
    #  T1  T2            T2  T3
    x = y.izq
    T2 = x.der
    x.der = y
    y.izq = T2
    self._actualizar_altura(y)
    self._actualizar_altura(x)
    return x

def _rebalancear(self, nodo):
    fb = self._factor_balance(nodo)
    if fb > 1 and self._factor_balance(nodo.izq) >= 0:
        return self.rotacion_der(nodo)       # Izquierda-Izquierda
    if fb > 1 and self._factor_balance(nodo.izq) < 0:
        return self.rotacion_izq_der(nodo)   # Izquierda-Derecha
    if fb < -1 and self._factor_balance(nodo.der) <= 0:
        return self.rotacion_izq(nodo)       # Derecha-Derecha
    if fb < -1 and self._factor_balance(nodo.der) > 0:
        return self.rotacion_der_izq(nodo)   # Derecha-Izquierda
    return nodo
```

---

## SLIDE 7 — AXEL · Pila

**¿Qué es?**
Estructura **LIFO** (Last In, First Out): el último en entrar es el primero en salir.
Todas las operaciones son **O(1)**.

Dos implementaciones:
- `PilaEstatica` → arreglo de tamaño fijo
- `PilaDinamica` → nodos enlazados sin límite

**¿Qué resuelve en el proyecto?**
Implementa el botón **"Quitar último"** del panel de pedidos.
Cada producto agregado se apila; si el cliente se arrepiente, se desapila.
También la usa el algoritmo DFS del grafo.

**Archivo:** `estructuras/pila_dinamica.py`

```python
def apilar(self, dato):
    nuevo = Nodo(dato)
    nuevo.siguiente = self._tope   # el nuevo apunta al anterior tope
    self._tope = nuevo             # el tope ahora es el nuevo nodo

def desapilar(self):
    if self.esta_vacia():
        raise IndexError("Pila dinámica vacía")
    dato = self._tope.dato
    self._tope = self._tope.siguiente   # bajar el tope
    return dato
```

---

## SLIDE 8 — AXEL · Lista Doble y Lista Circular

**Lista Doble**
Cada nodo apunta al siguiente **y al anterior**.
Insertar/eliminar en cualquier extremo: **O(1)**.

**¿Qué resuelve?** Guarda el **historial de estados** de cada pedido.
(`creado → confirmado → despachado`)

```python
def insertar_final(self, dato):
    nuevo = NodoDoble(dato)
    nuevo.anterior = self.cola      # nuevo apunta al actual último
    self.cola.siguiente = nuevo     # actual último apunta al nuevo
    self.cola = nuevo               # nuevo es el último
```

---

**Lista Circular**
El último nodo apunta de vuelta al primero. No tiene fin.

**¿Qué resuelve?** Maneja los **turnos rotativos de repartidores**.
Al llegar al último, vuelve automáticamente al primero.

**Archivo:** `estructuras/lista_circular.py`

```python
def insertar(self, dato):
    nuevo = Nodo(dato)
    if self.esta_vacia():
        nuevo.siguiente = nuevo    # apunta a sí mismo
        self.ultimo = nuevo
    else:
        nuevo.siguiente = self.ultimo.siguiente  # nuevo → primero
        self.ultimo.siguiente = nuevo            # último → nuevo
        self.ultimo = nuevo                      # nuevo es el último

def siguiente_turno(self):
    self.ultimo = self.ultimo.siguiente   # rotar
    return self.ultimo.dato
```

---

## SLIDE 9 — AXEL · Grafo con BFS y DFS

**¿Qué es?**
Conjunto de vértices (zonas) conectados por aristas (rutas).
Implementado con **lista de adyacencia** (`GrafoLista`).

Zonas: `Local ↔ Norte ↔ Costanera ↔ Isla` y `Local ↔ Sur ↔ Costanera`

**¿Qué resuelve en el proyecto?**
- **BFS** (usa cola) → ruta con **menos paradas** hasta una zona
- **DFS** (usa pila) → **todas las zonas alcanzables** desde el local

**Archivo:** `estructuras/grafo.py`

```python
def bfs(self, origen, destino):
    cola = ColaSimple()
    cola.encolar([origen])          # la cola guarda rutas completas
    visitados = {origen}
    while not cola.esta_vacia():
        camino = cola.desencolar()
        nodo_actual = camino[-1]
        for vecino in self.obtener_vecinos(nodo_actual):
            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                if vecino == destino:
                    return nuevo_camino     # ruta más corta encontrada
                visitados.add(vecino)
                cola.encolar(nuevo_camino)
    return []

def dfs(self, origen):
    pila = PilaDinamica()
    pila.apilar(origen)
    visitados = []
    while not pila.esta_vacia():
        nodo = pila.desapilar()
        if nodo not in set(visitados):
            visitados.append(nodo)
            for vecino in reversed(self.obtener_vecinos(nodo)):
                pila.apilar(vecino)
    return visitados
```

---

## SLIDE 10 — ENRIQUE · Cola

**¿Qué es?**
Estructura **FIFO** (First In, First Out): el primero en entrar es el primero en salir.
Encolar y desencolar: **O(1)**.

Dos implementaciones:
- `ColaSimple` → nodos enlazados
- `ColaCircular` → arreglo fijo con índices módulo (%)

**¿Qué resuelve en el proyecto?**
- `ColaSimple` → gestiona los **pedidos normales en espera**
- `ColaCircular(3)` → **pizarra de últimos 3 despachados** (sobreescribe el más viejo)

**Archivo:** `estructuras/cola_simple.py`

```python
def encolar(self, dato):
    nuevo = Nodo(dato)
    if self.esta_vacia():
        self._frente = self._final = nuevo
    else:
        self._final.siguiente = nuevo   # agregar al final
        self._final = nuevo

def desencolar(self):
    dato = self._frente.dato
    self._frente = self._frente.siguiente   # avanzar el frente
    if self._frente is None:
        self._final = None
    return dato
```

---

**Cola Circular** — el truco del módulo:

```python
def encolar(self, dato):
    if self.esta_llena():
        # sobreescribe el más viejo y avanza el frente
        self._datos[self._final % self.capacidad] = dato
        self._frente = (self._frente + 1) % self.capacidad
        self._final  = (self._final  + 1) % self.capacidad
    else:
        self._datos[self._final] = dato
        self._final = (self._final + 1) % self.capacidad
        self._longitud += 1
```

---

## SLIDE 11 — ENRIQUE · Cola de Prioridad

**¿Qué es?**
Cola que despacha primero al elemento con **mayor prioridad**.
Implementada con un **heap binario mínimo** guardado en un arreglo.

Para el nodo en índice `i`:
- Hijo izquierdo: `2i + 1`
- Hijo derecho: `2i + 2`
- Padre: `(i - 1) // 2`

Encolar y desencolar: **O(log n)**

**¿Qué resuelve en el proyecto?**
Cola de **pedidos urgentes**. Urgente = prioridad 0, Normal = prioridad 1.
"Despachar siguiente" siempre saca al más urgente primero.

**Archivo:** `estructuras/cola_prioridad.py`

```python
def encolar(self, elemento, prioridad=1):
    entrada = (prioridad, self._contador, elemento)
    self._contador += 1
    self._heap.append(entrada)
    self._subir(len(self._heap) - 1)   # reordenar hacia arriba

def _subir(self, indice):
    while indice > 0:
        padre = (indice - 1) // 2
        if self._heap[indice] < self._heap[padre]:
            self._heap[indice], self._heap[padre] = (
                self._heap[padre], self._heap[indice]
            )
            indice = padre
        else:
            break

def desencolar(self):
    self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
    _, _, elemento = self._heap.pop()
    if self._heap:
        self._bajar(0)        # reordenar hacia abajo
    return elemento
```

---

## SLIDE 12 — ENRIQUE · Árbol ABB

**¿Qué es?**
Árbol Binario de Búsqueda: izquierda < nodo < derecha.
Buscar, insertar y eliminar: **O(log n)** si está balanceado.

**Eliminación con dos hijos** → busca el **sucesor inorden**
(el menor del subárbol derecho), copia su clave y lo elimina.

**¿Qué resuelve en el proyecto?**
Es la base del AVL. Los recorridos **inorden, preorden y postorden**
están implementados y se visualizan en la pestaña "Estructuras".

**Archivo:** `estructuras/abb.py`

```python
def _insertar(self, nodo, codigo, producto):
    if nodo is None:
        return NodoArbol(codigo, producto)
    if codigo < nodo.codigo:
        nodo.izq = self._insertar(nodo.izq, codigo, producto)
    elif codigo > nodo.codigo:
        nodo.der = self._insertar(nodo.der, codigo, producto)
    else:
        nodo.producto = producto   # actualizar si ya existe
    return nodo

def _eliminar(self, nodo, codigo):
    # ... (casos hoja, un hijo)
    # Caso dos hijos: reemplazar con sucesor inorden
    sucesor = self._minimo(nodo.der)
    nodo.codigo   = sucesor.codigo
    nodo.producto = sucesor.producto
    nodo.der = self._eliminar(nodo.der, sucesor.codigo)
    return nodo

def inorden(self):
    # izquierda → raíz → derecha → devuelve ordenado de menor a mayor
    resultado = []
    self._inorden(self.raiz, resultado)
    return resultado
```

---

## SLIDE 13 — Tabla resumen

| Persona | 🟢 Fácil | 🟡 Media | 🔴 Difícil |
|---------|----------|----------|------------|
| **Lucas** | Nodo | Lista Simple | Árbol AVL |
| **Axel** | Pila | Lista Doble / Circular | Grafo BFS/DFS |
| **Enrique** | Cola | Cola de Prioridad | Árbol ABB |

---

## SLIDE 14 — Complejidades

| Estructura | Insertar | Buscar | Eliminar |
|------------|----------|--------|----------|
| Lista Simple | O(1) inicio / O(n) final | O(n) | O(n) |
| Lista Doble | O(1) extremos | O(n) | O(1) con ref |
| Pila / Cola | O(1) | — | O(1) |
| Cola Prioridad (heap) | O(log n) | — | O(log n) |
| ABB | O(log n) promedio | O(log n) | O(log n) |
| AVL | O(log n) siempre | O(log n) | O(log n) |
| Grafo BFS/DFS | — | O(V + A) | — |

---

## SLIDE 15 — Cierre

**Lo que aprendimos:**
- Implementar estructuras desde cero obliga a entender cada detalle interno
- Elegir la estructura correcta para cada problema impacta directamente en la eficiencia
- El AVL resuelve el peor caso del ABB; la Cola de Prioridad resuelve el orden de atención justo

**El proyecto corre con:**
```
python main.py
```
