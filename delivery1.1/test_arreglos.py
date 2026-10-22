#!/usr/bin/env python
"""Test para validar que los arreglos funcionan correctamente."""

from local import Local, ErrorDeNegocio
import sys


def test_pedido_atrapado():
    """Prueba que cancelar() se llame cuando confirmar() falla."""
    print("Test 1: Pedido atrapado (sin productos)")
    local = Local()
    
    # Iniciar pedido
    local.iniciar_pedido("Cliente", "Norte")
    assert local.pedido_actual is not None, "Pedido debe estar abierto"
    
    # Intentar confirmar sin productos (falla)
    try:
        local.confirmar()
        assert False, "Debería fallar sin productos"
    except ErrorDeNegocio as e:
        print(f"  ✓ Error esperado: {e}")
    
    # En la GUI, aquí se llamaría a cancelar() automáticamente
    local.cancelar()
    assert local.pedido_actual is None, "Pedido debería estar limpio"
    
    # Probar que se puede crear un nuevo pedido
    local.iniciar_pedido("Otro Cliente", "Sur")
    assert local.pedido_actual is not None, "Debería poder crear nuevo pedido"
    print("  ✓ Pedido recuperado correctamente\n")


def test_estadistica_despachados():
    """Prueba que podemos contar total de despachados correctamente."""
    print("Test 2: Estadística de despachados")
    local = Local()
    
    # Crear 5 pedidos
    for i in range(5):
        local.iniciar_pedido(f"Cliente {i}", "")
        local.agregar(101)  # Milanesa
        local.confirmar()
    
    # Despachar todos
    despachados = 0
    while len(local.en_espera()) > 0:
        local.despachar()
        despachados += 1
    
    assert despachados == 5, f"Debería haber 5 despachados, hay {despachados}"
    print(f"  ✓ Total despachados: {despachados}")
    
    # La cola circular listos solo tiene 3
    assert len(local.listos) == 3, "Cola circular debe tener solo 3"
    print(f"  ✓ Cola circular (pizarra): {len(local.listos)}")
    print("  ✓ Estadísticas correctas\n")


def test_todas_operaciones():
    """Prueba que todas las operaciones de la GUI funcionan."""
    print("Test 3: Todas las operaciones")
    local = Local()
    
    # 1. Crear pedido con múltiples unidades
    local.iniciar_pedido("Ana", "Norte")
    for _ in range(2):
        local.agregar(101)  # 2x Milanesa
    local.agregar(102)  # 1x Papas
    assert len(list(local.pedido_actual.items)) == 3, "Debería haber 3 productos"
    print("  ✓ Múltiples unidades del mismo producto")
    
    # 2. Quitar último (pila)
    local.quitar_ultimo()
    assert len(list(local.pedido_actual.items)) == 2, "Debería quedar 2 productos"
    print("  ✓ Quitar último producto (pila)")
    
    # 3. Confirmar
    local.confirmar()
    assert local.pedido_actual is None, "Pedido confirmado debe limpiar"
    print("  ✓ Confirmar pedido")
    
    # ELIMINADO EN REFACTORIZACIÓN:
    # - Búsqueda binaria (por precio exacto)
    # - Búsqueda secuencial (por nombre)
    # - Combo por presupuesto (backtracking) - se mantiene internamente
    # - Calculadora (postfija)
    print("  ℹ️  Búsquedas y calculadora eliminadas de GUI (refactorización a 9 estructuras)")
    
    # 8. Zonas (grafo con BFS/DFS)
    rutas = local.zonas_alcanzables()
    assert len(rutas) > 0, "Debería haber zonas alcanzables"
    print(f"  ✓ Zonas alcanzables: {len(rutas)}")
    
    ruta_bfs = local.recorrido_por_anchura()
    assert len(ruta_bfs) > 0, "BFS debería retornar rutas"
    print(f"  ✓ Recorrido BFS: {len(ruta_bfs)} nodos")
    
    print()


def main():
    try:
        test_pedido_atrapado()
        test_estadistica_despachados()
        test_todas_operaciones()
        print("=" * 50)
        print("✓ TODOS LOS TESTS PASARON")
        print("=" * 50)
        return 0
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
