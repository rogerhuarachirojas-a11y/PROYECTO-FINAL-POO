class Combo:
    DESCUENTO = 0.10   
    def __init__(self, nombre, productos=None, descuento=DESCUENTO):
        if not nombre:
            raise ValueError("El combo necesita un nombre")
        if not 0 <= descuento < 1:
            raise ValueError("El descuento debe estar entre 0 y 1 (0.10 = 10%)")
        self._nombre = nombre
        self._descuento = descuento
        self._productos = []
        for producto in (productos or []):
            self.agregar_producto(producto)
    @property
    def nombre(self):
        return self._nombre

    @property
    def descuento(self):
        return self._descuento

    @property
    def productos(self):
        return tuple(self._productos)

    def agregar_producto(self, producto):
        if producto is None:
            raise ValueError("El combo necesita un producto")
        if producto in self._productos:
            raise ValueError(f"{producto.nombre} ya esta en el combo")
        self._productos.append(producto)
        producto.combo = self

    def calcular_precio(self):
        total = 0
        for producto in self._productos:
            total = total + producto.calcular_precio()
        return round(total * (1 - self._descuento), 2)

    def contar_platos(self):
        cantidad = 0
        for producto in self._productos:
            cantidad = cantidad + producto.contar_platos()
        return cantidad

    def esta_disponible(self, dia):
        if len(self._productos) == 0:
            return False
        for producto in self._productos:
            if not producto.esta_disponible(dia):
                return False
        return True
    DESCUENTO = 0.10   # 10%

    def __init__(self, nombre, productos=None, descuento=DESCUENTO):
        if not nombre:
            raise ValueError("El combo necesita un nombre")
        if not 0 <= descuento < 1:
            raise ValueError("El descuento debe estar entre 0 y 1 (0.10 = 10%)")
        self._nombre = nombre
        self._descuento = descuento
        self._productos = []
        for producto in (productos or []):
            self.agregar_producto(producto)
    @property
    def nombre(self):
        return self._nombre

    @property
    def descuento(self):
        return self._descuento
    @property
    def productos(self):
        return tuple(self._productos)

    def agregar_producto(self, producto):
        if producto is None:
            raise ValueError("El combo necesita un producto")
        if producto in self._productos:
            raise ValueError(f"{producto.nombre} ya esta en el combo")
        self._productos.append(producto)
        producto.combo = self
    def calcular_precio(self):
        total = 0
        for producto in self._productos:
            total = total + producto.calcular_precio()
        return round(total * (1 - self._descuento), 2)

    def contar_platos(self):
        cantidad = 0
        for producto in self._productos:
            cantidad = cantidad + producto.contar_platos()
        return cantidad
    def esta_disponible(self, dia):
        if len(self._productos) == 0:
            return False
        for producto in self._productos:
            if not producto.esta_disponible(dia):
                return False
        return True