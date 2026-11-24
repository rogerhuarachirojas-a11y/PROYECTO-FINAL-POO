# DetalleComboPedido: detalle de un producto (o combo) con su cantidad y precio.
# Se relaciona solo con Producto.
class DetalleComboPedido:
    def __init__(self, producto, cantidad):
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > 20:
            raise ValueError("La cantidad debe ser un entero entre 1 y 20")
        self._producto = producto
        self._cantidad = cantidad
        self._precio = round(producto.calcular_precio(), 2)

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio(self):
        return self._precio

    def calcular_subtotal(self):
        return round(self._precio * self._cantidad, 2)

    def disponible(self, dia):
        return self._producto.esta_disponible(dia)

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad