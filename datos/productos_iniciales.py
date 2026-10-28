"""
Catálogo inicial de productos.
Se usa para cargar el AVL al iniciar la aplicación.
"""

from modelos import Producto

PRODUCTOS_INICIALES = [
    Producto(101, "Hamburguesa Simple", 1500.0, "comida"),
    Producto(102, "Hamburguesa Doble",  2200.0, "comida"),
    Producto(103, "Pizza Muzzarella",   2800.0, "comida"),
    Producto(104, "Pizza Especial",     3500.0, "comida"),
    Producto(105, "Papas Fritas",        900.0, "comida"),
    Producto(106, "Panchos",             800.0, "comida"),
    Producto(107, "Gaseosa Lata",        600.0, "bebida"),
    Producto(108, "Gaseosa 1.5L",       1100.0, "bebida"),
    Producto(109, "Cerveza 473ml",       900.0, "bebida"),
    Producto(110, "Cerveza 1L",         1600.0, "bebida"),
]
