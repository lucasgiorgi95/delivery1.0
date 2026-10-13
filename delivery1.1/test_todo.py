import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algoritmos import backtracking, busqueda, ordenamiento, postfija
from estructuras.arbol import ABB, AVL
from estructuras.cola import ColaCircular, ColaSimple
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.grafo import GrafoLista, GrafoMatriz, bfs, camino_con_menos_paradas, dfs
from estructuras.listas import ListaCircular, ListaDoble, ListaSimple
from estructuras.pila import PilaDinamica, PilaEstatica
from local import ErrorDeNegocio, Local
from modelos import Producto


class TestPilas(unittest.TestCase):
    def prueba(self, pila):
        for x in (1, 2, 3):
            pila.apilar(x)
        self.assertEqual(pila.ver_tope(), 3)
        self.assertEqual([pila.desapilar() for _ in range(3)], [3, 2, 1])   # LIFO
        self.assertTrue(pila.esta_vacia())
        with self.assertRaises(IndexError):
            pila.desapilar()

    def test_estatica(self):
        self.prueba(PilaEstatica(5))

    def test_dinamica(self):
        self.prueba(PilaDinamica())

    def test_estatica_llena(self):
        p = PilaEstatica(2)
        p.apilar(1)
        p.apilar(2)
        with self.assertRaises(OverflowError):
            p.apilar(3)


class TestColas(unittest.TestCase):
    def test_simple_fifo(self):
        c = ColaSimple()
        for x in "abc":
            c.encolar(x)
        self.assertEqual([c.desencolar() for _ in range(3)], ["a", "b", "c"])
        self.assertTrue(c.esta_vacia())
        c.encolar("z")                    # se puede volver a usar tras vaciarse
        self.assertEqual(c.ver_frente(), "z")

    def test_circular_da_la_vuelta(self):
        c = ColaCircular(3)
        for x in (1, 2, 3):
            c.encolar(x)
        with self.assertRaises(OverflowError):
            c.encolar(4)
        self.assertEqual(c.desencolar(), 1)
        c.encolar(4)                      # reusa el lugar liberado
        self.assertEqual(list(c), [2, 3, 4])

    def test_prioridad(self):
        c = ColaPrioridad()
        for dato, prio in [("c", 3), ("a", 1), ("d", 3), ("b", 2)]:
            c.encolar(dato, prio)
        self.assertEqual(c.ver_frente(), "a")
        self.assertEqual(c.en_orden_de_salida(), ["a", "b", "c", "d"])   # c antes que d: llegó antes
        self.assertEqual([c.desencolar() for _ in range(4)], ["a", "b", "c", "d"])

    def test_prioridad_muchos_datos_sale_ordenado(self):
        azar = random.Random(3)
        c = ColaPrioridad()
        valores = [azar.randint(0, 50) for _ in range(200)]
        for v in valores:
            c.encolar(v, v)
        self.assertEqual([c.desencolar() for _ in range(200)], sorted(valores))


class TestListas(unittest.TestCase):
    def test_simple(self):
        l = ListaSimple()
        l.insertar_final(2)
        l.insertar_final(3)
        l.insertar_inicio(1)
        self.assertEqual(list(l), [1, 2, 3])
        self.assertTrue(l.eliminar(lambda x: x == 2))
        self.assertFalse(l.eliminar(lambda x: x == 99))
        self.assertEqual(l.eliminar_ultimo(), 3)
        self.assertEqual(list(l), [1])
        self.assertEqual(len(l), 1)

    def test_doble_ambos_sentidos(self):
        l = ListaDoble()
        for x in (2, 3):
            l.insertar_final(x)
        l.insertar_inicio(1)
        self.assertEqual(list(l), [1, 2, 3])
        self.assertEqual(list(l.iter_inverso()), [3, 2, 1])
        self.assertEqual(l.eliminar_ultimo(), 3)
        self.assertEqual(list(l.iter_inverso()), [2, 1])

    def test_circular_turnos(self):
        l = ListaCircular()
        for x in "ABC":
            l.insertar(x)
        self.assertEqual([l.siguiente_turno() for _ in range(7)], list("ABCABCA"))
        self.assertEqual(len(l), 3)


class TestArboles(unittest.TestCase):
    def armar(self, clase):
        a = clase()
        for k in (50, 30, 70, 20, 40, 60, 80):
            a.insertar(k, str(k))
        return a

    def test_recorridos(self):
        a = self.armar(ABB)
        self.assertEqual([k for k, _ in a.inorden()], [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual([k for k, _ in a.preorden()], [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual([k for k, _ in a.postorden()], [20, 40, 30, 60, 80, 70, 50])

    def test_buscar_y_reemplazar(self):
        a = self.armar(ABB)
        self.assertEqual(a.buscar(60), "60")
        self.assertIsNone(a.buscar(65))
        a.insertar(60, "nuevo")
        self.assertEqual(a.buscar(60), "nuevo")
        self.assertEqual(len(a), 7)

    def test_eliminar_los_tres_casos(self):
        for clase in (ABB, AVL):
            a = self.armar(clase)
            a.eliminar(20)                                    # hoja
            a.eliminar(30)                                    # un hijo
            a.eliminar(50)                                    # dos hijos (la raíz)
            self.assertEqual([k for k, _ in a.inorden()], [40, 60, 70, 80])
            self.assertEqual(len(a), 4)
            with self.assertRaises(KeyError):
                a.eliminar(999)

    def test_abb_se_degenera_y_avl_no(self):
        abb, avl = ABB(), AVL()
        for k in range(100):
            abb.insertar(k)
            avl.insertar(k)
        self.assertEqual(abb.altura(), 100)
        self.assertLessEqual(avl.altura(), 8)                  # ~log2(100)
        self.assertEqual([k for k, _ in avl.inorden()], list(range(100)))
        self.assertGreater(avl.rotaciones, 0)

    def test_avl_equilibrado_con_altas_y_bajas_al_azar(self):
        azar = random.Random(7)
        avl = AVL()
        claves = azar.sample(range(1000), 300)
        for k in claves:
            avl.insertar(k)
        for k in claves[:150]:
            avl.eliminar(k)

        def revisar(n):
            if n is None:
                return 0
            hi, hd = revisar(n.izq), revisar(n.der)
            self.assertLessEqual(abs(hi - hd), 1)
            return 1 + max(hi, hd)
        revisar(avl.raiz)
        self.assertEqual([k for k, _ in avl.inorden()], sorted(claves[150:]))


class TestGrafos(unittest.TestCase):
    def armar(self, clase):
        g = clase()
        for a, b in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]:
            g.agregar_arista(a, b)
        g.agregar_vertice("Z")
        return g

    def test_ambas_representaciones_dan_lo_mismo(self):
        for clase in (GrafoMatriz, GrafoLista):
            g = self.armar(clase)
            self.assertTrue(g.hay_arista("A", "B"))
            self.assertTrue(g.hay_arista("B", "A"))
            self.assertFalse(g.hay_arista("A", "D"))
            self.assertEqual(sorted(g.vecinos("D")), ["B", "C", "E"])
            self.assertEqual(bfs(g, "A"), ["A", "B", "C", "D", "E"])
            self.assertEqual(dfs(g, "A"), ["A", "B", "D", "C", "E"])
            self.assertEqual(len(camino_con_menos_paradas(g, "A", "E")), 4)
            self.assertIsNone(camino_con_menos_paradas(g, "A", "Z"))

    def test_arista_repetida_no_duplica(self):
        g = GrafoLista()
        g.agregar_arista("A", "B")
        g.agregar_arista("B", "A")
        self.assertEqual(g.vecinos("A"), ["B"])


class TestAlgoritmos(unittest.TestCase):
    def test_ordenamientos(self):
        azar = random.Random(5)
        casos = [[], [1], [2, 1], list(range(30)), list(range(30, 0, -1)),
                 [azar.randint(0, 20) for _ in range(150)]]
        for nombre, f in ordenamiento.ALGORITMOS.items():
            for caso in casos:
                copia = list(caso)
                self.assertEqual(f(caso), sorted(caso), nombre)
                self.assertEqual(caso, copia, f"{nombre} no debe modificar la lista original")

    def test_ordenar_con_clave_y_estabilidad_del_mergesort(self):
        datos = [("b", 2), ("a", 2), ("c", 1)]
        self.assertEqual(ordenamiento.mergesort(datos, clave=lambda t: t[1]),
                         [("c", 1), ("b", 2), ("a", 2)])
        self.assertEqual([t[1] for t in ordenamiento.quicksort(datos, clave=lambda t: t[1])], [1, 2, 2])

    def test_busquedas(self):
        lista = [2, 5, 8, 12, 16, 23]
        for x in lista + [1, 9, 99]:
            esperado = lista.index(x) if x in lista else -1
            self.assertEqual(busqueda.secuencial(lista, x), esperado)
            self.assertEqual(busqueda.binaria(lista, x), esperado)
            self.assertEqual(busqueda.binaria_recursiva(lista, x), esperado)
        self.assertEqual(busqueda.binaria([], 1), -1)

    def test_postfija(self):
        self.assertEqual(postfija.infija_a_postfija("(1500 + 2500) * 90 / 100"),
                         ["1500", "2500", "+", "90", "*", "100", "/"])
        self.assertEqual(postfija.calcular("(1500+2500)*90/100"), 3600)
        self.assertEqual(postfija.calcular("2 + 3 * 4 - 6 / 2"), 11)
        for mala in ("2 +", "(2 + 3", "2 + 3)", "4 / 0", "2 $ 3"):
            with self.assertRaises(ValueError, msg=mala):
                postfija.calcular(mala)

    def test_backtracking(self):
        ps = [Producto(1, "a", 5), Producto(2, "b", 3), Producto(3, "c", 4)]
        combo = backtracking.armar_combo(ps, 7)
        self.assertEqual(sum(p.precio for p in combo), 7)
        self.assertIsNone(backtracking.armar_combo(ps, 2))
        self.assertEqual(sum(p.precio for p in backtracking.armar_combo(ps, 12)), 12)


class TestLocal(unittest.TestCase):
    def setUp(self):
        self.l = Local()

    def pedido(self, cliente, codigo, zona="", urgente=False, minutos=15):
        self.l.iniciar_pedido(cliente, zona)
        self.l.agregar(codigo)
        return self.l.confirmar(urgente, minutos)

    def test_catalogo(self):
        self.assertEqual([p.codigo for p in self.l.productos_por_codigo()], [101, 102, 103, 104, 105, 106, 107])
        precios = [p.precio for p in self.l.productos_por_precio()]
        self.assertEqual(precios, sorted(precios))
        self.assertEqual(self.l.buscar_por_precio(3500).nombre, "Cerveza")
        self.assertIsNone(self.l.buscar_por_precio(1))
        self.assertEqual(self.l.buscar_por_nombre("HELADO").codigo, 106)

    def test_quitar_ultimo(self):
        self.l.iniciar_pedido("Ana")
        self.l.agregar(101)
        self.l.agregar(104)
        self.assertEqual(self.l.quitar_ultimo().codigo, 104)
        self.assertEqual(self.l.pedido_actual.total(), 5500)
        self.l.quitar_ultimo()
        with self.assertRaises(ErrorDeNegocio):
            self.l.quitar_ultimo()

    def test_normales_salen_por_orden_de_llegada(self):
        for c in ("Ana", "Beto", "Cami"):
            self.pedido(c, 101)
        self.assertEqual([self.l.despachar().cliente for _ in range(3)], ["Ana", "Beto", "Cami"])

    def test_urgentes_primero_y_entre_urgentes_el_mas_apurado(self):
        self.pedido("Normal", 101)
        self.pedido("Urgente20", 101, urgente=True, minutos=20)
        self.pedido("Urgente5", 101, urgente=True, minutos=5)
        self.assertEqual([p.cliente for p in self.l.en_espera()], ["Urgente5", "Urgente20", "Normal"])
        self.assertEqual([self.l.despachar().cliente for _ in range(3)], ["Urgente5", "Urgente20", "Normal"])

    def test_repartidores_rotan_y_retiro_no_usa_repartidor(self):
        for c in range(4):
            self.pedido(f"c{c}", 101, zona="Norte")
        self.pedido("Retira", 101)
        self.assertEqual([self.l.despachar().repartidor for _ in range(4)], ["Rosa", "Tomás", "Lucía", "Rosa"])
        self.assertIsNone(self.l.despachar().repartidor)

    def test_pizarra_circular_guarda_los_ultimos_3(self):
        for c in range(5):
            self.pedido(f"c{c}", 101)
        for _ in range(5):
            self.l.despachar()
        self.assertEqual([p.cliente for p in self.l.listos], ["c2", "c3", "c4"])

    def test_historial_doble(self):
        self.pedido("Ana", 101)
        p = self.l.despachar()
        self.assertEqual(list(p.historial), ["Confirmado", "Despachado"])
        self.assertEqual(list(p.historial.iter_inverso()), ["Despachado", "Confirmado"])

    def test_zonas(self):
        self.assertEqual(self.l.ruta("Costanera"), ["Local", "Centro", "Norte", "Costanera"])
        self.assertIsNone(self.l.ruta("Isla"))
        self.assertNotIn("Isla", self.l.zonas_alcanzables())
        self.l.iniciar_pedido("Ana", "Isla")
        self.l.agregar(101)
        with self.assertRaises(ErrorDeNegocio):
            self.l.confirmar()

    def test_errores_con_mensaje(self):
        for accion in (lambda: self.l.agregar(101), lambda: self.l.confirmar(),
                       lambda: self.l.cancelar(), lambda: self.l.despachar(),
                       lambda: self.l.iniciar_pedido("  "), lambda: self.l.calcular("2 +")):
            with self.assertRaises(ErrorDeNegocio):
                accion()
        self.l.iniciar_pedido("Ana")
        with self.assertRaises(ErrorDeNegocio):
            self.l.iniciar_pedido("Beto")
        with self.assertRaises(ErrorDeNegocio):
            self.l.agregar(999)
        with self.assertRaises(ErrorDeNegocio):
            self.l.confirmar()                      # pedido vacío

    def test_combo_y_calculadora(self):
        combo = self.l.combo(10000)
        self.assertEqual(sum(p.precio for p in combo), 10000)
        self.assertIsNone(self.l.combo(1))
        self.assertEqual(self.l.calcular("(5500 + 3000) * 90 / 100"), 7650)


if __name__ == "__main__":
    unittest.main()
