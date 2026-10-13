"""Unidades 3 y 7: cola de prioridad implementada con un heap (montículo) binario mínimo.

El heap es un árbol binario completo guardado en un arreglo: el hijo izquierdo de i está
en 2i+1, el derecho en 2i+2 y el padre en (i-1)//2. La raíz siempre es el menor.
encolar y desencolar son O(log n); ver_frente es O(1).
Ante igual prioridad sale primero el que llegó antes (se guarda un número de orden)."""


class ColaPrioridad:
    def __init__(self):
        self._heap = []          # elementos: (prioridad, orden de llegada, dato)
        self._orden = 0

    def encolar(self, dato, prioridad):
        """Menor número = más urgente."""
        self._heap.append((prioridad, self._orden, dato))
        self._orden += 1
        self._subir(len(self._heap) - 1)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola de prioridad está vacía")
        self._intercambiar(0, len(self._heap) - 1)
        _, _, dato = self._heap.pop()
        if self._heap:
            self._bajar(0)
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            raise IndexError("La cola de prioridad está vacía")
        return self._heap[0][2]

    def esta_vacia(self):
        return not self._heap

    def __len__(self):
        return len(self._heap)

    def en_orden_de_salida(self):
        """Lista de datos en el orden en que saldrían, sin modificar la cola (O(n log n))."""
        return [dato for _, _, dato in sorted(self._heap)]

    def _intercambiar(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _subir(self, i):
        while i > 0:
            padre = (i - 1) // 2
            if self._heap[i][:2] < self._heap[padre][:2]:
                self._intercambiar(i, padre)
                i = padre
            else:
                break

    def _bajar(self, i):
        n = len(self._heap)
        while True:
            menor = i
            for hijo in (2 * i + 1, 2 * i + 2):
                if hijo < n and self._heap[hijo][:2] < self._heap[menor][:2]:
                    menor = hijo
            if menor == i:
                break
            self._intercambiar(i, menor)
            i = menor
