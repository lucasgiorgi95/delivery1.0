"""Unidad 8: grafos no dirigidos, con las dos representaciones del programa, y recorridos.

- Matriz de adyacencia: matriz[i][j] = 1 si hay arista. Consultar si dos vértices están
  unidos es O(1), pero ocupa O(V^2) de memoria.
- Lista de adyacencia: cada vértice guarda la lista de sus vecinos. Ocupa O(V + A) y es
  mejor para grafos con pocas aristas (como un mapa de zonas).

Los recorridos funcionan con cualquiera de las dos: solo piden vecinos(vertice)."""
from estructuras.cola import ColaSimple
from estructuras.listas import ListaSimple
from estructuras.pila import PilaDinamica


class GrafoMatriz:
    def __init__(self):
        self._nombres = []
        self._indice = {}
        self._matriz = []

    def agregar_vertice(self, nombre):
        if nombre in self._indice:
            return
        self._indice[nombre] = len(self._nombres)
        self._nombres.append(nombre)
        for fila in self._matriz:
            fila.append(0)
        self._matriz.append([0] * len(self._nombres))

    def agregar_arista(self, a, b):
        self.agregar_vertice(a)
        self.agregar_vertice(b)
        i, j = self._indice[a], self._indice[b]
        self._matriz[i][j] = self._matriz[j][i] = 1

    def hay_arista(self, a, b):
        return self._matriz[self._indice[a]][self._indice[b]] == 1

    def vertices(self):
        return list(self._nombres)

    def vecinos(self, vertice):
        fila = self._matriz[self._indice[vertice]]
        return [self._nombres[j] for j, hay in enumerate(fila) if hay]


class GrafoLista:
    def __init__(self):
        self._adyacentes = {}          # vértice -> ListaSimple de vecinos

    def agregar_vertice(self, nombre):
        if nombre not in self._adyacentes:
            self._adyacentes[nombre] = ListaSimple()

    def agregar_arista(self, a, b):
        self.agregar_vertice(a)
        self.agregar_vertice(b)
        if not self.hay_arista(a, b):
            self._adyacentes[a].insertar_final(b)
            self._adyacentes[b].insertar_final(a)

    def hay_arista(self, a, b):
        return self._adyacentes[a].buscar(lambda v: v == b) is not None

    def vertices(self):
        return list(self._adyacentes)

    def vecinos(self, vertice):
        return list(self._adyacentes[vertice])


def bfs(grafo, origen):
    """Recorrido en anchura: visita primero todos los vecinos, luego los vecinos de los
    vecinos... Usa una COLA. Devuelve los vértices en el orden visitado."""
    visitados = {origen}
    orden = []
    cola = ColaSimple()
    cola.encolar(origen)
    while not cola.esta_vacia():
        v = cola.desencolar()
        orden.append(v)
        for w in grafo.vecinos(v):
            if w not in visitados:
                visitados.add(w)
                cola.encolar(w)
    return orden


def dfs(grafo, origen):
    """Recorrido en profundidad: sigue un camino hasta el fondo y vuelve atrás.
    Usa una PILA. Devuelve los vértices en el orden visitado."""
    visitados = set()
    orden = []
    pila = PilaDinamica()
    pila.apilar(origen)
    while not pila.esta_vacia():
        v = pila.desapilar()
        if v in visitados:
            continue
        visitados.add(v)
        orden.append(v)
        for w in reversed(grafo.vecinos(v)):     # reversed para visitar en el orden cargado
            if w not in visitados:
                pila.apilar(w)
    return orden


def camino_con_menos_paradas(grafo, origen, destino):
    """Aplicación de BFS: el primer camino que encuentra tiene la menor cantidad de
    aristas. Devuelve la lista de vértices o None si no hay camino."""
    padre = {origen: None}
    cola = ColaSimple()
    cola.encolar(origen)
    while not cola.esta_vacia():
        v = cola.desencolar()
        if v == destino:
            camino = []
            while v is not None:
                camino.append(v)
                v = padre[v]
            camino.reverse()
            return camino
        for w in grafo.vecinos(v):
            if w not in padre:
                padre[w] = v
                cola.encolar(w)
    return None
