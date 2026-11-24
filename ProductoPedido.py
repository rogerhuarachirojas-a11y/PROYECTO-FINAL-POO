# ProductoPedido: una linea del pedido (producto + cantidad). Ejemplo: "2 x Silpancho".
class ProductoPedido:
    def __init__(self, producto, cantidad):
        self._producto = producto
        self._precio_unitario = round(producto.calcular_precio(), 2)  # precio al agregarlo
        self._cantidad = cantidad
        if not self.validar_cantidad():
            raise ValueError("La cantidad debe ser un entero entre 1 y 20")

    # True si la cantidad es un entero de 1 a 20 (sin parametro revisa la cantidad actual)
    # MODIFICAR AQUI si cambia el limite
    def validar_cantidad(self, cantidad=None):
        if cantidad is None:
            cantidad = self._cantidad
        return isinstance(cantidad, int) and 1 <= cantidad <= 20

    @property
    def producto(self):
        return self._producto

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if not self.validar_cantidad(valor):
            raise ValueError("La cantidad debe ser un entero entre 1 y 20")
        self._cantidad = valor

    def calcular_sub(self):
        return round(self._precio_unitario * self._cantidad, 2)

    # Platos de la linea (si es un combo, cuenta los platos de adentro)
    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad

