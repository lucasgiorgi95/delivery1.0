"""Sistema de pedidos - Local de Comidas (TP Estructura de Datos)"""
from gui import main


def plata(n):
    return "$" + f"{n:,.0f}".replace(",", ".")


def linea(titulo):
    print(f"\n--- {titulo} ---")


def mostrar_pedido(p):
    print(f"  Pedido #{p.id} de {p.cliente} ({p.zona}){'  [URGENTE]' if p.urgente else ''}")
    if p.items.esta_vacia():
        print("    (sin productos todavía)")
    for item in p.items:
        print(f"    - {item.nombre}  {plata(item.precio)}")
    print(f"  TOTAL: {plata(p.total())}")


def mostrar_catalogo(productos):
    for p in productos:
        print(f"  {p.codigo}  {p.nombre:<20} {plata(p.precio):>8}")


def pedir(texto):
    return input(texto).strip()


# ---------------------------------------------------------------- menú interactivo
def menu_pedido(local):
    try:
        local.iniciar_pedido(pedir("Nombre del cliente: "),
                             pedir("Zona de entrega (Enter si retira en el local): "))
    except ErrorDeNegocio as e:
        print("  Atención:", e)
        return
    while True:
        linea("Elegí el código del producto")
        mostrar_catalogo(local.productos_por_codigo())
        print("  D) Quitar el último   C) Cancelar pedido   F) Confirmar pedido")
        op = pedir("Opción: ").upper()
        try:
            if op.isdigit():
                local.agregar(int(op))
            elif op == "D":
                local.quitar_ultimo()
            elif op == "C":
                if pedir("¿Seguro que querés cancelar? (s/n): ").lower() == "s":
                    local.cancelar()
                    print("  Pedido cancelado.")
                    return
                continue
            elif op == "F":
                urgente = pedir("¿Es urgente? (s/n): ").lower() == "s"
                minutos = 15
                if urgente:
                    texto = pedir("¿En cuántos minutos se prometió? (Enter = 15): ")
                    minutos = int(texto) if texto.isdigit() else 15
                p = local.confirmar(urgente, minutos)
                print(f"  Listo: pedido #{p.id} confirmado por {plata(p.total())}.")
                return
            else:
                print("  No entendí. Escribí un código, D, C o F.")
                continue
        except ErrorDeNegocio as e:
            print("  Atención:", e)
        mostrar_pedido(local.pedido_actual)


def menu_catalogo(local):
    linea("Catálogo")
    print("1) Por código  2) Por precio  3) Buscar por precio exacto  4) Buscar por nombre")
    op = pedir("Opción: ")
    if op == "1":
        mostrar_catalogo(local.productos_por_codigo())
    elif op == "2":
        mostrar_catalogo(local.productos_por_precio())
    elif op == "3":
        texto = pedir("Precio: ")
        p = local.buscar_por_precio(int(texto)) if texto.isdigit() else None
        print("  ", f"{p.nombre} ({plata(p.precio)})" if p else "Ningún producto cuesta eso.")
    elif op == "4":
        p = local.buscar_por_nombre(pedir("Nombre completo: "))
        print("  ", f"{p.codigo} - {p.nombre} ({plata(p.precio)})" if p else "No encontré ese producto.")


def menu_zonas(local):
    linea("Zonas de entrega")
    print("  Zonas con envío:", ", ".join(local.zonas_alcanzables()))
    zona = pedir("Ver ruta a (Enter para volver): ")
    if zona:
        ruta = local.ruta(zona) if zona in local.zonas.vertices() else None
        print("  ", " -> ".join(ruta) if ruta else f"No hay ruta a «{zona}».")


def menu_combo(local):
    texto = pedir("Presupuesto del cliente: ")
    combo = local.combo(int(texto)) if texto.isdigit() else None
    if combo:
        print("  Combo:", ", ".join(p.nombre for p in combo), "=", plata(sum(p.precio for p in combo)))
    else:
        print("  No hay una combinación que sume justo eso.")


def menu_calculadora(local):
    cuenta = pedir("Cuenta (ej: (5500 + 3000) * 90 / 100): ")
    try:
        print("  Resultado:", plata(local.calcular(cuenta)))
    except ErrorDeNegocio as e:
        print("  Atención:", e)


def menu_complejidad():
    linea("Tiempos de ordenamiento (segundos)")
    tamanios, tabla = medir.tabla_ordenamiento()
    print("  " + " " * 11 + "".join(f"n={n:<10}" for n in tamanios))
    for nombre, tiempos in tabla.items():
        print(f"  {nombre:<11}" + "".join(f"{t:<12.5f}" for t in tiempos))
    n, seq, bin_ = medir.comparar_busquedas()
    print(f"\n  Buscar entre {n} elementos: secuencial {seq:.1f} µs, binaria {bin_:.2f} µs")
    n, h_abb, h_avl, rot = medir.comparar_arboles()
    print(f"  {n} claves ordenadas: altura ABB = {h_abb}, altura AVL = {h_avl} ({rot} rotaciones)")


def menu_estructuras():
    """Menú para ver estructuras de datos y su complejidad."""
    while True:
        linea("Estructuras de Datos y Complejidad")
        print("1) Ver todas las estructuras")
        print("2) Ver información de una estructura específica")
        print("0) Volver")
        op = pedir("Opción: ")
        
        if op == "1":
            print("\nEstructuras disponibles:")
            estructuras = listar_todas()
            for i, est in enumerate(estructuras, 1):
                print(f"  {i}. {est}")
        
        elif op == "2":
            print("\nEstructuras disponibles:")
            estructuras = listar_todas()
            for i, est in enumerate(estructuras, 1):
                print(f"  {i}. {est}")
            
            try:
                idx = int(pedir("Seleccione el número: ")) - 1
                if 0 <= idx < len(estructuras):
                    nombre = estructuras[idx]
                    info = info_estructura(nombre)
                    
                    print(f"\n{'='*70}")
                    print(f"{nombre}")
                    print(f"{'='*70}")
                    print(f"\nDescripción:\n  {info['descripcion']}")
                    print(f"\nOperaciones principales:\n  {info['operacion']}")
                    print(f"\nCOMPLEJIDAD ASINTÓTICA:")
                    print(f"  • Big O (peor caso):     {info['big_o']}")
                    print(f"  • Theta (promedio):      {info['theta']}")
                    print(f"  • Omega (mejor caso):    {info['omega']}")
                    print(f"\nUsos en este local:")
                    for uso in info['usos']:
                        print(f"  • {uso}")
                else:
                    print("  Opción inválida")
            except (ValueError, IndexError):
                print("  Opción inválida")
        
        elif op == "0":
            break
        else:
            print("  No entendí. Escribí un número del menú.")


def mostrar_espera(local):
    linea("Pedidos en espera (en orden de despacho)")
    espera = local.en_espera()
    if not espera:
        print("  No hay pedidos en espera.")
    for i, p in enumerate(espera, 1):
        print(f"  {i}. #{p.id} {p.cliente} ({p.zona}) {plata(p.total())}{'  [URGENTE]' if p.urgente else ''}")
    if len(local.listos):
        print("  Últimos despachados:", ", ".join(f"#{p.id} {p.cliente}" for p in local.listos))


def menu(local):
    while True:
        print("\n=== PEDIDOS DEL LOCAL ===")
        print(f"Pedidos en espera: {len(local.en_espera())}")
        print("1) Nuevo pedido     2) Despachar el siguiente   3) Ver pedidos en espera")
        print("4) Catálogo         5) Zonas de entrega         6) Armar combo por presupuesto")
        print("7) Calculadora      8) Medir complejidad        9) Ver estructuras")
        print("0) Salir")
        op = pedir("Opción: ")
        try:
            if op == "1":
                menu_pedido(local)
            elif op == "2":
                p = local.despachar()
                quien = f" con {p.repartidor}" if p.repartidor else " (retira en el local)"
                print(f"  Despachado: #{p.id} de {p.cliente}{quien}.")
            elif op == "3":
                mostrar_espera(local)
            elif op == "4":
                menu_catalogo(local)
            elif op == "5":
                menu_zonas(local)
            elif op == "6":
                menu_combo(local)
            elif op == "7":
                menu_calculadora(local)
            elif op == "8":
                menu_complejidad()
            elif op == "9":
                menu_estructuras()
            elif op == "0":
                break
            else:
                print("  No entendí. Escribí un número del menú.")
        except ErrorDeNegocio as e:
            print("  Atención:", e)
        except (EOFError, KeyboardInterrupt):
            break


# ---------------------------------------------------------------- demo automática
def demo():
    local = Local()
    linea("1. Catálogo en un AVL (insertado en desorden) -> recorrido inorden = por código")
    mostrar_catalogo(local.productos_por_codigo())
    print("  preorden:", [c for c, _ in local.catalogo.preorden()])
    print("  postorden:", [c for c, _ in local.catalogo.postorden()])
    print("  altura del árbol:", local.catalogo.altura(), "con", len(local.catalogo), "productos")

    linea("2. Pedido de Ana: lista simple + pila para quitar el último")
    local.iniciar_pedido("Ana", "Norte")
    for codigo in (101, 103, 104, 104):
        local.agregar(codigo)
    local.quitar_ultimo()
    mostrar_pedido(local.pedido_actual)
    local.confirmar()

    linea("3. Más pedidos: normal (cola) y urgente (cola de prioridad / heap)")
    for cliente, zona, codigo, urgente, minutos in [("Beto", "", 105, False, 0),
                                                     ("Cami", "Sur", 102, True, 20),
                                                     ("Dani", "Costanera", 107, True, 10)]:
        local.iniciar_pedido(cliente, zona)
        local.agregar(codigo)
        local.confirmar(urgente, minutos)
    mostrar_espera(local)

    linea("4. Despacho: urgentes primero; repartidores rotan (lista circular)")
    despachados = []
    for _ in range(4):
        p = local.despachar()
        despachados.append(p)
        print(f"  #{p.id} {p.cliente} -> {p.repartidor or 'retira en el local'}")
    mostrar_espera(local)
    print("  (la pizarra circular guarda solo los últimos 3 de los 4 despachados)")
    p = despachados[0]
    print(f"  Historial del pedido #{p.id} (lista doble):", " -> ".join(p.historial),
          "| al revés:", " -> ".join(p.historial.iter_inverso()))

    linea("5. Zonas: grafo con lista de adyacencia")
    print("  BFS desde el local:", local.recorrido_por_anchura())
    print("  DFS desde el local:", local.zonas_alcanzables())
    print("  Ruta con menos paradas a Costanera:", " -> ".join(local.ruta("Costanera")))
    print("  Ruta a Isla:", local.ruta("Isla"))

    linea("6. Catálogo por precio (mergesort) y búsquedas")
    mostrar_catalogo(local.productos_por_precio())
    print("  Binaria, precio 3500:", local.buscar_por_precio(3500))
    print("  Secuencial, 'helado':", local.buscar_por_nombre("helado"))

    linea("7. Pilas: combo por presupuesto (backtracking) y calculadora (postfija)")
    combo = local.combo(10000)
    print("  Combo de", plata(10000), "->", [p.nombre for p in combo])
    print("  Combo de", plata(1), "->", local.combo(1))
    print("  (5500 + 3000) * 90 / 100 =", plata(local.calcular("(5500 + 3000) * 90 / 100")))

    linea("8. Complejidad medida")
    menu_complejidad()


if __name__ == "__main__":
    from gui import main as gui_main
    gui_main()
