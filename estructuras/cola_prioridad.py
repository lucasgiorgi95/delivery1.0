"""
Cola de Prioridad implementada con heap binario mínimo.
Cada elemento se guarda como tupla (prioridad, orden_llegada, elemento).
El elemento con menor número de prioridad sale primero.
Ante empate de prioridad, sale el que llegó antes (orden_llegada menor).
"""


class ColaPrioridad:
    """
    Heap binario mínimo guardado en lista Python.
    Para el nodo en índice i:
      - hijo izquierdo: 2*i + 1
      - hijo derecho:   2*i + 2
      - padre:          (i - 1) // 2
    """

    def __init__(self):
        self._heap = []          # lista de tuplas (prioridad, orden, elemento)
        self._contador = 0       # desempate por orden de llegada

    def esta_vacia(self):
        return len(self._heap) == 0

    def longitud(self):
        return len(self._heap)

    # ── operaciones internas del heap ──────────

    def _subir(self, indice):
        """Sube el nodo en 'indice' hasta su posición correcta."""
        while indice > 0:
            padre = (indice - 1) // 2
            if self._heap[indice] < self._heap[padre]:
                self._heap[indice], self._heap[padre] = (
                    self._heap[padre], self._heap[indice]
                )
                indice = padre
            else:
                break

    def _bajar(self, indice):
        """Baja el nodo en 'indice' hasta su posición correcta."""
        n = len(self._heap)
        while True:
            menor = indice
            izq = 2 * indice + 1
            der = 2 * indice + 2
            if izq < n and self._heap[izq] < self._heap[menor]:
                menor = izq
            if der < n and self._heap[der] < self._heap[menor]:
                menor = der
            if menor != indice:
                self._heap[indice], self._heap[menor] = (
                    self._heap[menor], self._heap[indice]
                )
                indice = menor
            else:
                break

    # ── operaciones públicas ────────────────────

    def encolar(self, elemento, prioridad=1):
        """
        Inserta 'elemento' con la prioridad dada.
        prioridad=0 → urgente  /  prioridad=1 → normal
        """
        entrada = (prioridad, self._contador, elemento)
        self._contador += 1
        self._heap.append(entrada)
        self._subir(len(self._heap) - 1)

    def desencolar(self):
        """Elimina y devuelve el elemento con menor prioridad."""
        if self.esta_vacia():
            raise IndexError("Cola de prioridad vacía")
        # Intercambia raíz con último elemento y baja la nueva raíz
        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        _, _, elemento = self._heap.pop()
        if self._heap:
            self._bajar(0)
        return elemento

    def ver_tope(self):
        """Mira el elemento con mayor prioridad sin extraerlo."""
        if self.esta_vacia():
            return None
        return self._heap[0][2]

    def obtener_todos(self):
        """
        Devuelve lista Python con los elementos ordenados por prioridad
        (sin modificar el heap).
        """
        ordenado = sorted(self._heap)
        return [elem for (_, _, elem) in ordenado]

    def __repr__(self):
        items = self.obtener_todos()
        return "ColaPrioridad[" + ", ".join(str(x) for x in items) + "]"
