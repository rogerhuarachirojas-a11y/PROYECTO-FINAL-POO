<<<<<<< HEAD
from __future__ import annotations

from typing import TYPE_CHECKING

from Producto import Producto
from Combo import Combo

if TYPE_CHECKING:
    from Pedido import Pedido

class DetalleComboPedido:
    CANTIDAD_MAXIMA = 20

    def __init__(self, producto: Producto | Combo, cantidad: int, id_pedido: str, pedido: Pedido):
        if not isinstance(producto, (Producto, Combo)):
            raise ValueError("El detalle necesita un producto o un combo")
        if not id_pedido:
            raise ValueError("El detalle necesita el id del pedido")
        if pedido is None:
            raise ValueError("El detalle necesita un pedido")
        self._producto = producto
        self._id_pedido = str(id_pedido)
        self._pedido = pedido
        # Se guarda el precio del momento: si el combo cambia despues, este pedido no cambia
        self._precio = producto.calcular_precio()
        self.cantidad = cantidad   # pasa por el setter, que valida el rango

    # ---- Propiedades ----
=======
# DetalleComboPedido: detalle de un producto (o combo) con su cantidad y precio.
# Se relaciona solo con Producto.
class DetalleComboPedido:
    def __init__(self, producto, cantidad):
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > 20:
            raise ValueError("La cantidad debe ser un entero entre 1 y 20")
        self._producto = producto
        self._cantidad = cantidad
        self._precio = round(producto.calcular_precio(), 2)

>>>>>>> c90222d7b7ff5f63a623ae0d48ad58ccc6192aa1
    @property
    def producto(self):
        return self._producto

    @property
<<<<<<< HEAD
    def id_pedido(self):
        return self._id_pedido

    @property
    def pedido(self):
        return self._pedido
=======
    def cantidad(self):
        return self._cantidad
>>>>>>> c90222d7b7ff5f63a623ae0d48ad58ccc6192aa1

    @property
    def precio(self):
        return self._precio

<<<<<<< HEAD
    @property
    def cantidad(self):
        return self._cantidad

    # La cantidad debe ser un entero entre 1 y CANTIDAD_MAXIMA
    @cantidad.setter
    def cantidad(self, nueva):
        if not isinstance(nueva, int) or nueva < 1 or nueva > DetalleComboPedido.CANTIDAD_MAXIMA:
            raise ValueError(f"La cantidad debe estar entre 1 y {DetalleComboPedido.CANTIDAD_MAXIMA}")
        self._cantidad = nueva

    # ---- Calculos ----

    # Subtotal de la linea: precio x cantidad
    def calcular_sub(self):
        return round(self._precio * self._cantidad, 2)

    # Platos de la linea (platos dentro del combo x cantidad). Se usa para los envases
    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad

    # ---- Detalle ----

    # Texto de la linea para mostrar en el detalle del pedido
    def descripcion(self):
        return f"{self._cantidad} x {self._producto.nombre} - Bs {self.calcular_sub():.2f}"
=======
    def calcular_subtotal(self):
        return round(self._precio * self._cantidad, 2)

    def disponible(self, dia):
        return self._producto.disponible(dia)

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad
>>>>>>> c90222d7b7ff5f63a623ae0d48ad58ccc6192aa1
