# Pedidos de un local de comidas (TP integrador, Estructura de Datos)

Programa de consola en Python 3 (sin librerías externas) donde cada estructura del
programa de la materia resuelve una parte real de un local: armar pedidos, ponerlos en
cola, despacharlos, repartirlos por zonas y consultar el catálogo.
Las estructuras están programadas a mano; no se usan `deque`, `heapq` ni `bisect`. El
`sorted` de Python aparece solo en las pruebas (para comprobar resultados) y en
`ColaPrioridad.en_orden_de_salida`, que únicamente sirve para mostrar la fila en pantalla.

## Cómo correrlo

```
python main.py          # interfaz gráfica completa
python main.py --demo   # recorrido automático (consola)
python -m unittest discover tests   # 32 pruebas
```

## Cambios en la GUI (v2)

### Problemas solucionados

1. **✓ Pedido atrapado**: Si `confirmar()` falla (sin productos o zona sin ruta), se llama automáticamente a `cancelar()` para liberar el pedido.

2. **✓ Estadística engañosa**: Se agregó contador `total_despachados` que persiste en toda la sesión. Ahora muestra el total real, no solo los 3 de la pizarra circular.

3. **✓ Funciones fuera de ventana**: Reorganización completa:
   - **Panel izquierdo**: Armado de pedidos, productos cargados, pedidos en espera, despacho
   - **Pestaña "Búsquedas"**: Búsqueda por precio (binaria), por nombre (secuencial), combo por presupuesto (backtracking)
   - **Pestaña "Calculadora"**: Evaluador de expresiones postfijas
   - **Pestaña "Zonas"**: Mapa de rutas con BFS
   - **Pestaña "Estructuras"**: Información de complejidad

4. **✓ Demo incompleta**: Botón "📊 Cargar Demo" carga automáticamente 4 pedidos y los despacha, mostrando:
   - Pila: quitar el último producto
   - Cola de prioridad: pedidos urgentes
   - Cola simple: pedidos normales
   - Cola circular: últimos 3 despachados
   - Repartidores (lista circular): asignación rotativa

5. **✓ Código viejo**: `main.py` limpiado. Solo llama a la GUI. El menú y demo de consola se mantienen como funciones auxiliares pero no se usan en ejecución normal.

### Nueva interfaz

| Zona | Contenido | Funcionalidad |
|------|-----------|--------------|
| **Panel izquierdo superior** | Formulario de armado | Cliente, zona, código+cantidad, urgencia, minutos |
| **Panel izquierdo centro** | Productos cargados | Lista con total acumulado |
| **Panel izquierdo bajo** | Pedidos en espera | Lista ordenada: urgentes primero |
| **Pestaña Catálogo** | Productos por código | AVL ordenado |
| **Pestaña Búsquedas** | 3 búsquedas | Binaria (precio exacto), secuencial (nombre), backtracking (combo) |
| **Pestaña Calculadora** | Evaluador postfijo | Convierte infija a postfija y calcula |
| **Pestaña Zonas** | Mapa de rutas | BFS + rutas cortas |
| **Pestaña Estadísticas** | Métricas | Pedidos, dinero, total despachados (correctamente), árbol AVL |
| **Pestaña Estructuras** | Complejidad | Dropdown de 16 estructuras con O/Θ/Ω |

### Acciones implementadas

- ✓ Quitar último producto (pila)
- ✓ Cancelar pedido
- ✓ Agregar múltiples unidades del mismo producto
- ✓ Búsqueda binaria por precio exacto
- ✓ Búsqueda secuencial por nombre
- ✓ Combo por presupuesto (backtracking)
- ✓ Calculadora postfija
- ✓ Cargar demo con 4 pedidos

## Mapa: programa de la materia -> dónde está -> para qué sirve

| Unidad | Tema del programa | Archivo | Problema que resuelve en el local |
|---|---|---|---|
| 1 | TAD | cada clase expone solo sus operaciones (apilar, encolar, insertar...) | Se usa sin saber cómo está hecha por dentro |
| 1 | Complejidad / Big O | `medir.py`, comentarios de cada clase | Menú 8: tiempos reales de ordenamiento, búsqueda y árboles |
| 2 | Estructuras autorreferenciadas | `estructuras/nodo.py` | Base de pilas, colas y listas |
| 3 | Pila estática y dinámica | `estructuras/pila.py` | «Quitar el último» producto (dinámica) |
| 3 | Notación postfija | `algoritmos/postfija.py` | Calculadora de caja: `(5500+3000)*90/100` |
| 3 | Backtracking con pila | `algoritmos/backtracking.py` | Combo que suma justo el presupuesto del cliente |
| 3 | Cola simple | `estructuras/cola.py` | Pedidos normales, por orden de llegada |
| 3 | Cola circular | `estructuras/cola.py` | Pizarra de «últimos 3 pedidos despachados» |
| 3 y 7 | Cola de prioridad (heap) | `estructuras/cola_prioridad.py` | Pedidos urgentes: sale primero el más apurado |
| 4 | Lista simple | `estructuras/listas.py` | Productos de un pedido |
| 4 | Lista doble | `estructuras/listas.py` | Historial de estados del pedido, en ambos sentidos |
| 4 | Lista circular | `estructuras/listas.py` | Turnos rotativos de repartidores |
| 5 | Burbuja, selección, inserción, shell, quicksort, mergesort | `algoritmos/ordenamiento.py` | Catálogo por precio (mergesort); comparación en el menú 8 |
| 6 | Búsqueda secuencial | `algoritmos/busqueda.py` | Producto por nombre (no hay orden por nombre) |
| 6 | Búsqueda binaria | `algoritmos/busqueda.py` | Producto por precio exacto (catálogo ya ordenado) |
| 7 | Árbol binario, ABB, recorridos | `estructuras/arbol.py` | Catálogo por código; inorden, preorden, postorden |
| 7 | AVL (introducción) | `estructuras/arbol.py` | Mantiene el catálogo equilibrado con rotaciones |
| 8 | Grafo: matriz y lista de adyacencia | `estructuras/grafo.py` | Mapa de zonas (lista); la matriz está para comparar |
| 8 | BFS | `estructuras/grafo.py` | Ruta con menos paradas hasta una zona |
| 8 | DFS | `estructuras/grafo.py` | Qué zonas se pueden alcanzar desde el local |

## Estructura de carpetas

```
tp_ed/
├── main.py              menú de consola y modo --demo
├── local.py             el negocio: junta todas las estructuras (sin print ni input)
├── modelos.py           Producto y Pedido
├── medir.py             mediciones de complejidad
├── estructuras/         nodo, pila, cola, cola_prioridad, listas, arbol, grafo
├── algoritmos/          ordenamiento, busqueda, postfija, backtracking
└── tests/test_todo.py
```

## Cosas para decir con honestidad en la explicación

- Para marcar «visitados» en los grafos se usa `set` de Python y para nombrar vértices un
  `dict`; las estructuras que importan (cola en BFS, pila en DFS, lista de adyacencia) son propias.
- `ListaSimple.insertar_final` es O(n) a propósito (solo guarda la cabeza): el `Pedido` lo usa
  porque tiene pocos productos. Con una cola de punteros sería O(1).
- El backtracking es exponencial en el peor caso (O(2^n)); con 7 productos no se nota.
- El heap usa un arreglo, no nodos; el AVL no está pensado para uso masivo, es la introducción.
- Los datos viven en memoria: al cerrar el programa se pierden los pedidos.

## Reparto sugerido (de a 2)

- **Persona A:** pilas, colas, cola de prioridad, listas, `modelos.py`, postfija, backtracking.
- **Persona B:** árboles (ABB/AVL), grafos, ordenamiento, búsqueda, `medir.py`.
- **Juntos:** `local.py`, `main.py`, pruebas y la explicación. Cada uno tiene que poder
  explicar también las piezas del otro.
