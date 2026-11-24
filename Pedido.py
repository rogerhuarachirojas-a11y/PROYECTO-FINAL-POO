from abc import ABC, abstractmethod
from datetime import datetime

from ProductoPedido import ProductoPedido


# Pedido: clase abstracta. Se usa Local, Llevar o Delivery.
class Pedido(ABC):
    REGISTRADO = "Registrado"
    EN_PREPARACION = "En preparacion"
    LISTO = "Listo"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"

    # Desde cada estado, a cuales se puede pasar (solo se cancela desde Registrado)
    # MODIFICAR AQUI si cambian las transiciones
    TRANSICIONES = {
        "Registrado": ["En preparacion", "Cancelado"],
        "En preparacion": ["Listo"],
        "Listo": ["Entregado"],
        "Entregado": [],
        "Cancelado": [],
    }

    DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

    def __init__(self, id_pedido, cliente, fecha=None):
        if not id_pedido:
            raise ValueError("El pedido necesita un id")
        if cliente is None:
            raise ValueError("El pedido necesita un cliente")
        self._id_pedido = str(id_pedido)
        self._cliente = cliente
        self._productos = []
        self._estado = Pedido.REGISTRADO
        self._fecha = fecha or datetime.now()

    @property
    def id_pedido(self):
        return self._id_pedido

    @property
    def cliente(self):
        return self._cliente

    @property
    def estado(self):
        return self._estado

    @property
    def fecha(self):
        return self._fecha

    # Devuelve una copia: nadie modifica la lista desde fuera
    @property
    def productos(self):
        return tuple(self._productos)

    def _buscar_linea(self, producto):
        for linea in self._productos:
            if linea.producto is producto:
                return linea
        return None

    # Solo en estado Registrado y si el producto se vende ese dia.
    # Si el producto ya estaba, se suma la cantidad.
    def agregar_pro(self, p, cant=1):
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden agregar productos en estado Registrado")
        dia = Pedido.DIAS[self._fecha.weekday()]
        if not p.disponible(dia):
            raise ValueError(f"{p.nombre} no esta disponible el {dia}")
        linea = self._buscar_linea(p)
        if linea is None:
            self._productos.append(ProductoPedido(p, cant))
        else:
            linea.cantidad = linea.cantidad + cant

    # Solo en estado Registrado
    def quitar_pro(self, p):
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden quitar productos en estado Registrado")
        linea = self._buscar_linea(p)
        if linea is None:
            raise ValueError("El producto no esta en el pedido")
        self._productos.remove(linea)

    # Cambia el estado solo si la transicion es valida (cancelar = cambiar a Cancelado)
    def cambiar_estado(self, est):
        if est not in Pedido.TRANSICIONES[self._estado]:
            raise ValueError(f"Cambio de estado invalido: {self._estado} -> {est}")
        if est == Pedido.EN_PREPARACION and len(self._productos) == 0:
            raise ValueError("No se puede preparar un pedido sin productos")
        self._estado = est

    # Subtotal: cada linea calcula el suyo (sin if por tipo de producto)
    def calcular_sub(self):
        total = 0
        for linea in self._productos:
            total = total + linea.calcular_sub()
        return round(total, 2)

    # Platos del pedido, incluidos los de dentro de combos (se usa para los envases)
    def contar_platos(self):
        cantidad = 0
        for linea in self._productos:
            cantidad = cantidad + linea.contar_platos()
        return cantidad

    # Cada tipo de pedido calcula su cargo extra
    @abstractmethod
    def calcular_recargo(self):
        pass

    def calcular_total(self):
        return round(self.calcular_sub() + self.calcular_recargo(), 2)