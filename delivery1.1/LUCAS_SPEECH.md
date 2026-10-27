# 🟦 Speech de Lucas — Guía de Exposición

> Estudiá esto antes de exponer. No lo leas en voz alta: usalo para saber qué decir en cada parte.

---

## 🟢 Nodo — `estructuras/nodo.py`

**Mini concepto**
Un nodo es el bloque más básico de las estructuras dinámicas. Guarda un dato y una referencia al siguiente nodo del mismo tipo. A eso lo llamamos estructura autorreferenciada. También existe el NodoDoble, que además apunta al nodo anterior.

**Qué soluciona en el proyecto y por qué se eligió**
Sin el nodo no podría existir ninguna estructura dinámica del proyecto. Se eligió porque permite que las estructuras crezcan o se achiquen en tiempo de ejecución sin desperdiciar memoria, algo que un arreglo de tamaño fijo no puede hacer. Cada producto que el cliente agrega al pedido ocupa exactamente un nodo, ni más ni menos.

**Dónde y cómo se usa**
Se usa en todas las estructuras dinámicas del proyecto: la pila, la cola simple y las listas. Cada vez que se agrega un producto a un pedido, internamente se crea un nodo nuevo que guarda ese producto. El NodoDoble aparece en el historial del pedido: cada estado por el que pasa un pedido (confirmado, despachado) queda guardado en un nodo doble dentro de la ListaDoble.

**En qué parte del código está**
Está definido en `estructuras/nodo.py`. Lo usan directamente `estructuras/listas.py`, `estructuras/pila.py` y `estructuras/cola.py`. Cada vez que esas estructuras hacen un insertar o apilar, crean un Nodo internamente.

---

## 🟡 Lista Simple — `estructuras/listas.py`

**Mini concepto**
Es una cadena de nodos donde cada uno apunta solo al siguiente. Solo se guarda el primer nodo, la cabeza. Insertar al inicio es inmediato (O(1)), pero insertar al final requiere recorrer toda la cadena (O(n)). También permite eliminar un elemento si se cumple alguna condición, sin necesidad de conocer su posición.

**Qué soluciona en el proyecto y por qué se eligió**
Soluciona el problema de que un pedido puede tener cualquier cantidad de productos. No se sabe de antemano si el cliente va a pedir uno o diez ítems. Se eligió la lista simple porque el orden de carga importa (se muestra al cliente tal como lo fue agregando) y porque no se necesita recorrer hacia atrás. El costo de insertar al final siendo O(n) es aceptable porque los pedidos no tienen cientos de productos.

**Dónde y cómo se usa**
Se usa en dos lugares del proyecto. El primero y más importante es dentro de cada Pedido: el atributo `items` es una ListaSimple que guarda los productos en el orden en que el cliente los fue agregando. Cada vez que se presiona "Agregar" en la pantalla, el producto se inserta al final de esa lista. Cuando se presiona "Quitar último", se elimina el último nodo. El segundo lugar es dentro del Grafo: cada zona del mapa guarda sus zonas vecinas en una ListaSimple.

**En qué parte del código está**
La estructura está en `estructuras/listas.py`, clase `ListaSimple`. Se instancia en `modelos.py` dentro de la clase `Pedido` como `self.items = ListaSimple()`. También la usa `estructuras/grafo.py` para guardar los vecinos de cada zona.

---

## 🔴 Árbol AVL — `estructuras/arbol.py`

**Mini concepto**
El AVL es un Árbol Binario de Búsqueda que se autobalancea. En un ABB común, cada nodo tiene a la izquierda claves menores y a la derecha claves mayores, lo que permite buscar en O(log n). El problema es que si los datos se insertan en orden, el árbol se convierte en una lista y la búsqueda se vuelve O(n). El AVL lo evita: después de cada inserción o eliminación, verifica si alguna rama quedó demasiado alta y la corrige con rotaciones, garantizando siempre O(log n).

**Qué soluciona en el proyecto y por qué se eligió**
Soluciona el almacenamiento del catálogo de productos con búsqueda rápida por código. Se eligió el AVL en lugar del ABB simple porque los productos del catálogo tienen códigos consecutivos (101, 102, 103...). Si se cargaran en ese orden en un ABB, el árbol degeneraría en una lista y cada búsqueda sería lenta. El AVL garantiza que sin importar el orden de carga, el árbol siempre queda equilibrado y la búsqueda es siempre O(log n).

**Dónde y cómo se usa**
Se usa de tres formas en el proyecto. Primero, al arrancar el sistema se cargan los 7 productos del catálogo en el AVL. Segundo, cada vez que se agrega un producto a un pedido, el sistema busca el producto por su código en el AVL para validar que exista y obtener su nombre y precio. Tercero, la pestaña "Catálogo" de la interfaz muestra todos los productos ordenados de menor a mayor código, lo cual se obtiene haciendo un recorrido inorden del AVL, que por definición devuelve los nodos en orden ascendente.

**En qué parte del código está**
La estructura está en `estructuras/arbol.py`, clases `ABB` y `AVL` (el AVL hereda del ABB). Se instancia en `local.py` dentro de la clase `Local` como `self.catalogo = AVL()`. El método `buscar` del AVL se llama en `local.py` cada vez que se agrega un producto. El método `inorden` se llama en `local.py` para listar el catálogo ordenado, y ese resultado es el que muestra la GUI en la pestaña Catálogo.

---

## 📋 Resumen rápido

| Estructura | Archivo | Usado en | Para qué |
|------------|---------|----------|----------|
| Nodo | `estructuras/nodo.py` | listas, pila, cola | Base de todas las estructuras dinámicas |
| Lista Simple | `estructuras/listas.py` | `modelos.py`, `grafo.py` | Guardar los productos de cada pedido |
| AVL | `estructuras/arbol.py` | `local.py` | Catálogo de productos con búsqueda O(log n) |
