"""Información de complejidad de las 9 estructuras de datos fundamentales del local."""

ESTRUCTURAS = {
    "1. Pila (Stack)": {
        "descripcion": "Última entrada, primera salida (LIFO)",
        "operacion": "apilar, desapilar",
        "big_o": "O(1)",
        "theta": "Θ(1)",
        "omega": "Ω(1)",
        "usos": [
            "Quitar el último producto del pedido",
            "Armar combo por presupuesto (usa backtracking)",
        ],
    },
    "2. Cola (Queue)": {
        "descripcion": "Primera entrada, primera salida (FIFO)",
        "operacion": "encolar, desencolar",
        "big_o": "O(1)",
        "theta": "Θ(1)",
        "omega": "Ω(1)",
        "usos": [
            "Pedidos normales en orden de llegada",
            "Cola circular: últimos 3 pedidos despachados",
        ],
    },
    "3. Cola de Prioridad (Heap)": {
        "descripcion": "Estructura de árbol binario para prioridades (min-heap)",
        "operacion": "insertar, extraer_min",
        "big_o": "O(log n)",
        "theta": "Θ(log n)",
        "omega": "Ω(1) insert, Ω(log n) extract",
        "usos": [
            "Pedidos urgentes: sale primero el más apurado (menos minutos)",
        ],
    },
    "4. Lista Simple": {
        "descripcion": "Nodos enlazados, recorrido en una dirección",
        "operacion": "insertar, eliminar, recorrer",
        "big_o": "O(n) insert_final, O(1) insert_inicio",
        "theta": "Θ(n) en promedio",
        "omega": "Ω(1)",
        "usos": [
            "Productos de un pedido actual",
        ],
    },
    "5. Lista Doble": {
        "descripcion": "Nodos enlazados, recorrido bidireccional (adelante/atrás)",
        "operacion": "insertar, eliminar, recorrer",
        "big_o": "O(n)",
        "theta": "Θ(n)",
        "omega": "Ω(1)",
        "usos": [
            "Historial de estados del pedido (creado, confirmado, despachado, etc.)",
        ],
    },
    "6. Lista Circular": {
        "descripcion": "Nodos enlazados en círculo, recorrido cíclico",
        "operacion": "insertar, rotar, siguiente_turno",
        "big_o": "O(1) rotar",
        "theta": "Θ(1)",
        "omega": "Ω(1)",
        "usos": [
            "Turnos rotativos de repartidores (Rosa → Tomás → Lucía → Rosa...)",
        ],
    },
    "7. Árbol AVL (Balanced BST)": {
        "descripcion": "Árbol binario auto-balanceado con rotaciones",
        "operacion": "buscar, insertar, eliminar",
        "big_o": "O(log n)",
        "theta": "Θ(log n)",
        "omega": "Ω(1)",
        "usos": [
            "Catálogo de productos ordenado por código",
            "Búsqueda rápida de productos: O(log n)",
        ],
    },
    "8. Grafo (Lista de Adyacencia)": {
        "descripcion": "Estructura para representar conexiones entre zonas",
        "operacion": "BFS, DFS, búsqueda de ruta",
        "big_o": "O(V + E)",
        "theta": "Θ(V + E)",
        "omega": "Ω(V) mejor caso",
        "usos": [
            "Mapa de zonas de entrega (Local, Centro, Norte, Sur, Costanera, Isla)",
            "Ruta con menos paradas (BFS): encuentra camino óptimo",
            "Zonas alcanzables desde el local (DFS): qué zonas se pueden alcanzar",
        ],
    },
    "9. Backtracking": {
        "descripcion": "Algoritmo que explora todas las combinaciones, retrocede si no funciona",
        "operacion": "buscar combinación que suma exactamente el presupuesto",
        "big_o": "O(2^n)",
        "theta": "Θ(2^n)",
        "omega": "Ω(1)",
        "usos": [
            "Armar combo de productos que suma exactamente el presupuesto del cliente",
            "Funcionalidad interna: no expuesta en la GUI como pestaña",
        ],
    },
}


def info_estructura(nombre):
    """Retorna la información de complejidad de una estructura."""
    return ESTRUCTURAS.get(nombre, None)


def listar_todas():
    """Retorna la lista de todas las 9 estructuras fundamentales."""
    return list(ESTRUCTURAS.keys())
