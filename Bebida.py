from Producto import Producto
class Bebida(Producto):
    JARRA = "Jarra"
    VASO = "Vaso"
    TAMANOS = (JARRA, VASO)
    def __init__(self, nombre, precio, precio_vaso, tamano, tipo, menu=None):
        super().__init__(nombre, precio, Producto.TODOS_LOS_DIAS, menu)
        if not Producto.verificar_precio(precio_vaso):
            raise ValueError("El precio del vaso debe ser un numero mayor a 0")
        if not tipo:
            raise ValueError("La bebida necesita un tipo")
        self._precio_vaso = float(precio_vaso)
        self._tamano = Bebida._validar_tamano(tamano)
        self._tipo = tipo
    @property
    def precio_vaso(self):
        return self._precio_vaso

    @property
    def tamano(self):
        return self._tamano

    @property
    def tipo(self):
        return self._tipo

    # ---- Validaciones ----

    # Acepta "jarra", "JARRA", "Vaso", etc. y devuelve el valor normalizado
    @staticmethod
    def _validar_tamano(tamano):
        normal = str(tamano).capitalize()
        if normal not in Bebida.TAMANOS:
            raise ValueError("El tamano debe ser Jarra o Vaso")
        return normal

    # Precio segun el tamano. Si no se indica, usa el tamano de la bebida
    def calcular_precio(self, tamano=None):
        if tamano is None:
            tamano = self._tamano
        else:
            tamano = Bebida._validar_tamano(tamano)
        if tamano == Bebida.VASO:
            return round(self._precio_vaso, 2)
        return round(self._precio, 2)