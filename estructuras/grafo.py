"""
Grafo no dirigido con lista de adyacencia (GrafoLista).
Implementa BFS (ruta más corta) y DFS (zonas alcanzables).
"""

from estructuras.lista_simple  import ListaSimple
from estructuras.cola_simple   import ColaSimple
from estructuras.pila_dinamica import PilaDinamica


class GrafoLista:
    """
    Grafo no dirigido representado con lista de adyacencia.
    Cada vértice es un string (nombre de zona).
    La adyacencia de cada vértice se guarda en una ListaSimple.
    """

    def __init__(self):
        # dict: nombre_vertice -> ListaSimple de vecinos
        self._adyacencia = {}

    def agregar_vertice(self, nombre):
        if nombre not in self._adyacencia:
            self._adyacencia[nombre] = ListaSimple()

    def agregar_arista(self, origen, destino):
        """Arista no dirigida: agrega en ambas direcciones."""
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        # Evitar duplicados
        vecinos_origen = self._adyacencia[origen].recorrer()
        if destino not in vecinos_origen:
            self._adyacencia[origen].insertar_final(destino)
        vecinos_destino = self._adyacencia[destino].recorrer()
        if origen not in vecinos_destino:
            self._adyacencia[destino].insertar_final(origen)

    def obtener_vertices(self):
        return list(self._adyacencia.keys())

    def obtener_vecinos(self, vertice):
        if vertice not in self._adyacencia:
            return []
        return self._adyacencia[vertice].recorrer()

    # ── BFS ────────────────────────────────────

    def bfs(self, origen, destino):
        """
        Recorrido BFS desde origen hasta destino.
        Devuelve la lista del camino más corto (en cantidad de paradas)
        o [] si no hay camino.
        """
        if origen not in self._adyacencia or destino not in self._adyacencia:
            return []
        if origen == destino:
            return [origen]

        visitados = set()
        cola = ColaSimple()
        # Cada elemento de la cola es la ruta hasta ese nodo
        cola.encolar([origen])
        visitados.add(origen)

        while not cola.esta_vacia():
            camino = cola.desencolar()
            nodo_actual = camino[-1]

            for vecino in self.obtener_vecinos(nodo_actual):
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    if vecino == destino:
                        return nuevo_camino
                    visitados.add(vecino)
                    cola.encolar(nuevo_camino)

        return []   # sin camino

    # ── DFS ────────────────────────────────────

    def dfs(self, origen):
        """
        Recorrido DFS desde origen.
        Devuelve lista de todas las zonas alcanzables (en orden de visita).
        """
        if origen not in self._adyacencia:
            return []

        visitados = []
        visitados_set = set()
        pila = PilaDinamica()
        pila.apilar(origen)

        while not pila.esta_vacia():
            nodo = pila.desapilar()
            if nodo not in visitados_set:
                visitados_set.add(nodo)
                visitados.append(nodo)
                # Apilar vecinos (en orden inverso para visitar el primero primero)
                vecinos = self.obtener_vecinos(nodo)
                for vecino in reversed(vecinos):
                    if vecino not in visitados_set:
                        pila.apilar(vecino)

        return visitados

    def __repr__(self):
        lineas = ["GrafoLista:"]
        for vertice, lista in self._adyacencia.items():
            vecinos = lista.recorrer()
            lineas.append(f"  {vertice} → {vecinos}")
        return "\n".join(lineas)
