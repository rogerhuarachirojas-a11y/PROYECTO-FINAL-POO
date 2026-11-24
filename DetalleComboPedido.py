class DetalleComboPedido:
    CANTIDAD_MAXIMA = 20

    def __init__(self, producto, cantidad, id_pedido, pedido):
        if producto is None:
            raise ValueError("El detalle necesita un producto")
        if not id_pedido:
            raise ValueError("El detalle necesita el id del pedido")
        if pedido is None:
            raise ValueError("El detalle necesita un pedido")
        self._producto = producto
        self._id_pedido = str(id_pedido)
        self._pedido = pedido
        # Se guarda el precio del momento: si el combo cambia despues, este pedido no cambia
        self._precio = producto.calcular_precio()
        self.cantidad = cantidad   
    @property
    def producto(self):
        return self._producto

    @property
    def id_pedido(self):
        return self._id_pedido

    @property
    def pedido(self):
        return self._pedido

    @property
    def precio(self):
        return self._precio

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva):
        if not isinstance(nueva, int) or nueva < 1 or nueva > DetalleComboPedido.CANTIDAD_MAXIMA:
            raise ValueError(f"La cantidad debe estar entre 1 y {DetalleComboPedido.CANTIDAD_MAXIMA}")
        self._cantidad = nueva

    def calcular_sub(self):
        return round(self._precio * self._cantidad, 2)

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad

    def descripcion(self):
        return f"{self._cantidad} x {self._producto.nombre} - Bs {self.calcular_sub():.2f}"