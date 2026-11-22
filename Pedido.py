from abc import ABC, abstractmethod
from datetime import datetime

from ProductoPedido import ProductoPedido
from DetalleComboPedido import DetalleComboPedido


# Pedido: clase abstracta. No se crea directo; se usa Local, Llevar o Delivery.
class Pedido(ABC):
    # Estados del pedido
    REGISTRADO = "Registrado"
    EN_PREPARACION = "En preparacion"
    LISTO = "Listo"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"

    # A que estados se puede pasar desde cada uno (solo se cancela desde Registrado)
    # MODIFICAR AQUI si cambian las transiciones
    TRANSICIONES = {
        "Registrado": ["En preparacion", "Cancelado"],
        "En preparacion": ["Listo"],
        "Listo": ["Entregado"],
        "Entregado": [],
        "Cancelado": [],
    }

    # Dias de la semana (weekday() da 0 para lunes)
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

    # Devuelve una copia para que nadie cambie la lista desde fuera
    @property
    def productos(self):
        return tuple(self._productos)

    # Busca la linea de un producto (None si no esta)
    def _buscar_linea(self, producto):
        for linea in self._productos:
            if linea.producto is producto:
                return linea
        return None

    # Revisa que se pueda agregar: estado Registrado y producto disponible hoy
    def _revisar_agregar(self, producto):
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden agregar productos en estado Registrado")
        dia = Pedido.DIAS[self._fecha.weekday()]
        if not producto.esta_disponible(dia):
            raise ValueError(f"{producto.nombre} no esta disponible el {dia}")

    # Agrega un producto; si ya estaba, suma la cantidad
    def agregar_pro(self, producto, cantidad=1):
        self._revisar_agregar(producto)
        linea = self._buscar_linea(producto)
        if linea is None:
            self._productos.append(ProductoPedido(producto, cantidad, self._id_pedido))
        else:
            linea.cantidad = linea.cantidad + cantidad

    # Igual, pero la linea es un DetalleComboPedido (guarda el pedido)
    def agregar_detalle(self, producto, cantidad=1):
        self._revisar_agregar(producto)
        linea = self._buscar_linea(producto)
        if linea is None:
            self._productos.append(DetalleComboPedido(producto, cantidad, self._id_pedido, self))
        else:
            linea.cantidad = linea.cantidad + cantidad

    # Quita un producto (solo en estado Registrado)
    def quitar_pro(self, producto):
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden quitar productos en estado Registrado")
        linea = self._buscar_linea(producto)
        if linea is None:
            raise ValueError("El producto no esta en el pedido")
        self._productos.remove(linea)

    # Subtotal = suma de los subtotales de cada linea
    def calcular_sub(self):
        total = 0
        for linea in self._productos:
            total = total + linea.calcular_sub()
        return round(total, 2)

    # Total de platos del pedido (cuenta los de dentro de combos)
    def contar_platos(self):
        cantidad = 0
        for linea in self._productos:
            cantidad = cantidad + linea.contar_platos()
        return cantidad

    # Metodo abstracto: cada tipo de pedido calcula su cargo extra
    @abstractmethod
    def calcular_recargo(self):
        pass

    # Total = subtotal + recargo
    def calcular_total(self):
        return round(self.calcular_sub() + self.calcular_recargo(), 2)

    # Cambia el estado si la transicion es valida; si no, lanza error
    def cambiar_estado(self, nuevo):
        if nuevo not in Pedido.TRANSICIONES[self._estado]:
            raise ValueError(f"Cambio de estado invalido: {self._estado} -> {nuevo}")
        if nuevo == Pedido.EN_PREPARACION and len(self._productos) == 0:
            raise ValueError("No se puede preparar un pedido sin productos")
        self._estado = nuevo

    # Cancelar = cambiar a Cancelado (solo se puede desde Registrado)
    def cancelar(self):
        self.cambiar_estado(Pedido.CANCELADO)

    # Texto con el detalle: productos, subtotal, cargos y total
    def mostrar_detalle(self):
        texto = f"Pedido {self._id_pedido} ({type(self).__name__}) - {self._estado}\n"
        for linea in self._productos:
            texto = texto + f"  {linea.cantidad} x {linea.producto.nombre}: Bs {linea.calcular_sub():.2f}\n"
        texto = texto + f"Subtotal: Bs {self.calcular_sub():.2f}\n"
        texto = texto + f"Cargos: Bs {self.calcular_recargo():.2f}\n"
        texto = texto + f"TOTAL: Bs {self.calcular_total():.2f}"
        return texto