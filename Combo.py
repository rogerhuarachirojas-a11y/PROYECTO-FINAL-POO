from Producto import Producto


# Combo: hereda de Producto y agrupa productos (platos y bebidas) con un descuento.
class Combo(Producto):
    DESCUENTO = 0.10   # 10%

    def __init__(self, nombre, productos=None, descuento=DESCUENTO, menu=None):
        if not nombre:
            raise ValueError("El combo necesita un nombre")
        if not 0 <= descuento < 1:
            raise ValueError("El descuento debe estar entre 0 y 1 (0.10 = 10%)")
        self._nombre = nombre
        self._descuento = descuento
        self._productos = []
        self._menu = list(menu) if menu else []
        self._combo = None
        for producto in (productos or []):
            self.agregar_producto(producto)
        self._precio = self.calcular_precio()
        self._disponible = "Segun productos del combo"

    # ---- Propiedades de solo lectura ----
    @property
    def descuento(self):
        return self._descuento

    # Devuelve una COPIA (tupla): desde fuera no se puede modificar la lista
    @property
    def productos(self):
        return tuple(self._productos)

    # ---- Manejo de productos ----

    # Agrega un producto al combo y le avisa al producto a que combo pertenece
    def agregar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise ValueError("El combo solo acepta productos (Plato, Bebida o Combo)")
        if producto is self:
            raise ValueError("Un combo no puede contenerse a si mismo")
        if producto in self._productos:
            raise ValueError(f"{producto.nombre} ya esta en el combo")
        self._productos.append(producto)
        producto.combo = self
        self._precio = self.calcular_precio()

    # ---- Calculos ----

    # Suma el precio de cada producto y le resta el descuento del combo
    def calcular_precio(self):
        total = 0
        for producto in self._productos:
            total = total + producto.calcular_precio()
        return round(total * (1 - self._descuento), 2)

    # Platos que hay dentro del combo (cada producto sabe cuantos cuenta)
    def contar_platos(self):
        cantidad = 0
        for producto in self._productos:
            cantidad = cantidad + producto.contar_platos()
        return cantidad

    # ---- Disponibilidad ----

    # El combo esta disponible solo si TODOS sus productos lo estan ese dia
    def esta_disponible(self, dia):
        if len(self._productos) == 0:
            return False
        for producto in self._productos:
            if not producto.esta_disponible(dia):
                return False
        return True
