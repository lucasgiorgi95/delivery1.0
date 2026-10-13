"""Información de complejidad de cada estructura de datos usada en el local."""

ESTRUCTURAS = {
    "Pila": {
        "descripcion": "Última entrada, primera salida (LIFO)",
        "operacion": "apilar, desapilar",
        "big_o": "O(1)",
        "theta": "Θ(1)",
        "omega": "Ω(1)",
        "usos": [
            "Quitar el último producto del pedido",
            "Combo por presupuesto (backtracking)",
            "Calculadora postfija",
        ],
    },
    "Cola": {
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
    "Cola de Prioridad (Heap)": {
        "descripcion": "Estructura de árbol binario para prioridades",
        "operacion": "insertar, extraer_min",
        "big_o": "O(log n)",
        "theta": "Θ(log n)",
        "omega": "Ω(1) insert, Ω(log n) extract",
        "usos": [
            "Pedidos urgentes: sale primero el más apurado",
        ],
    },
    "Lista Simple": {
        "descripcion": "Nodos enlazados, recorrido en una dirección",
        "operacion": "insertar, eliminar, recorrer",
        "big_o": "O(n) insert_final, O(1) insert_inicio",
        "theta": "Θ(n) en promedio",
        "omega": "Ω(1)",
        "usos": [
            "Productos de un pedido",
        ],
    },
    "Lista Doble": {
        "descripcion": "Nodos enlazados, recorrido bidireccional",
        "operacion": "insertar, eliminar, recorrer",
        "big_o": "O(n)",
        "theta": "Θ(n)",
        "omega": "Ω(1)",
        "usos": [
            "Historial de estados del pedido (antes/después)",
        ],
    },
    "Lista Circular": {
        "descripcion": "Nodos enlazados en círculo, recorrido cíclico",
        "operacion": "insertar, rotar",
        "big_o": "O(1) rotar",
        "theta": "Θ(1)",
        "omega": "Ω(1)",
        "usos": [
            "Turnos rotativos de repartidores",
        ],
    },
    "Árbol Binario de Búsqueda (ABB)": {
        "descripcion": "Árbol donde izq < padre < derecha",
        "operacion": "buscar, insertar, eliminar",
        "big_o": "O(n) peor caso",
        "theta": "Θ(log n) promedio",
        "omega": "Ω(1) búsqueda lucky",
        "usos": [
            "Catálogo por código",
        ],
    },
    "Árbol AVL": {
        "descripcion": "ABB auto-balanceado con rotaciones",
        "operacion": "buscar, insertar, eliminar",
        "big_o": "O(log n)",
        "theta": "Θ(log n)",
        "omega": "Ω(1)",
        "usos": [
            "Catálogo por código (mantiene balance)",
        ],
    },
    "Grafo - Lista de Adyacencia": {
        "descripcion": "Estructura para representar conexiones entre zonas",
        "operacion": "BFS, DFS, búsqueda de ruta",
        "big_o": "O(V + E)",
        "theta": "Θ(V + E)",
        "omega": "Ω(V) best case",
        "usos": [
            "Mapa de zonas de entrega",
            "Ruta con menos paradas (BFS)",
            "Zonas alcanzables desde el local (DFS)",
        ],
    },
    "Ordenamiento - Merge Sort": {
        "descripcion": "Divide y conquista: divide en mitades, ordena, fusiona",
        "operacion": "ordenar",
        "big_o": "O(n log n)",
        "theta": "Θ(n log n)",
        "omega": "Ω(n log n)",
        "usos": [
            "Catálogo ordenado por precio",
        ],
    },
    "Ordenamiento - Bubble Sort": {
        "descripcion": "Intercambia adyacentes si están mal ordenados",
        "operacion": "ordenar",
        "big_o": "O(n²)",
        "theta": "Θ(n²)",
        "omega": "Ω(n) si ya está ordenado",
        "usos": [
            "Comparación de complejidad (menú 8)",
        ],
    },
    "Ordenamiento - Quick Sort": {
        "descripcion": "Divide por pivote, ordena particiones",
        "operacion": "ordenar",
        "big_o": "O(n²) peor caso",
        "theta": "Θ(n log n) promedio",
        "omega": "Ω(n log n)",
        "usos": [
            "Comparación de complejidad (menú 8)",
        ],
    },
    "Búsqueda Secuencial": {
        "descripcion": "Recorre de inicio a fin hasta encontrar",
        "operacion": "buscar",
        "big_o": "O(n)",
        "theta": "Θ(n)",
        "omega": "Ω(1) found at start",
        "usos": [
            "Producto por nombre (sin ordenar)",
        ],
    },
    "Búsqueda Binaria": {
        "descripcion": "Divide por la mitad, descarta mitad innecesaria",
        "operacion": "buscar",
        "big_o": "O(log n)",
        "theta": "Θ(log n)",
        "omega": "Ω(1)",
        "usos": [
            "Producto por precio exacto (catálogo ordenado)",
        ],
    },
    "Backtracking": {
        "descripcion": "Explora todas las combinaciones, retrocede si no funciona",
        "operacion": "buscar combo",
        "big_o": "O(2^n)",
        "theta": "Θ(2^n)",
        "omega": "Ω(1)",
        "usos": [
            "Combo que suma justo el presupuesto del cliente",
        ],
    },
    "Notación Postfija": {
        "descripcion": "Convierte infija a postfija y evalúa",
        "operacion": "parsear y evaluar",
        "big_o": "O(n)",
        "theta": "Θ(n)",
        "omega": "Ω(n)",
        "usos": [
            "Calculadora de caja: (5500+3000)*90/100",
        ],
    },
}


def info_estructura(nombre):
    """Retorna la información de complejidad de una estructura."""
    return ESTRUCTURAS.get(nombre, None)


def listar_todas():
    """Retorna la lista de todas las estructuras."""
    return list(ESTRUCTURAS.keys())
