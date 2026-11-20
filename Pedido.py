from abc import ABC, abstractmethod
from datetime import datetime

from ProductoPedido import ProductoPedido
from DetalleComboPedido import DetalleComboPedido


# Pedido: clase ABSTRACTA (hereda de ABC y tiene un @abstractmethod).
# No se puede crear un Pedido directo; hay que usar Local, Llevar o Delivery.
class Pedido(ABC):
    REGISTRADO = "Registrado"
    EN_PREPARACION = "En preparacion"
    LISTO = "Listo"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"

    # A que estados se puede pasar desde cada estado.
    # Solo se puede cancelar desde Registrado. Cualquier otro cambio lanza error.
    TRANSICIONES = {
        "Registrado": ["En preparacion", "Cancelado"],
        "En preparacion": ["Listo"],
        "Listo": ["Entregado"],
        "Entregado": [],
        "Cancelado": [],
    }

    DIAS = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")

    ETIQUETA_RECARGO = "Cargos"

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

    # ---- Propiedades de solo lectura ----
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

    # Devuelve una COPIA (tupla): desde fuera no se puede modificar la lista de items
    @property
    def productos(self):
        return tuple(self._productos)

    # ---- Manejo de productos ----

    # Busca si el producto ya esta en el pedido; si no esta devuelve None
    def _buscar_linea(self, producto):
        for linea in self._productos:
            if linea.producto is producto:
                return linea
        return None

    # Revisa que se pueda agregar: estado Registrado y producto disponible ese dia
    def _validar_para_agregar(self, producto):
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden agregar productos en estado Registrado")
        dia = Pedido.DIAS[self._fecha.weekday()]
        # esta_disponible lo resuelve cada producto (el combo revisa los suyos)
        if not producto.esta_disponible(dia):
            raise ValueError(f"{producto.nombre} no esta disponible el {dia}")

    # Agrega un producto. Si ya estaba, suma la cantidad (el setter vuelve a validar el maximo de 20)
    def agregar_pro(self, producto, cantidad=1):
        self._validar_para_agregar(producto)
        linea = self._buscar_linea(producto)
        if linea is None:
            linea = ProductoPedido(producto, cantidad, self._id_pedido)
            self._productos.append(linea)
        else:
            linea.cantidad = linea.cantidad + cantidad
        return linea

    # Igual que agregar_pro pero la linea es un DetalleComboPedido (guarda el pedido)
    def agregar_detalle(self, producto, cantidad=1):
        self._validar_para_agregar(producto)
        linea = self._buscar_linea(producto)
        if linea is None:
            linea = DetalleComboPedido(producto, cantidad, self._id_pedido, self)
            self._productos.append(linea)
        else:
            linea.cantidad = linea.cantidad + cantidad
        return linea

    # Quita un producto del pedido (solo en estado Registrado)
    def quitar_pro(self, producto):
        if self._estado != Pedido.REGISTRADO:
            raise ValueError("Solo se pueden quitar productos en estado Registrado")
        linea = self._buscar_linea(producto)
        if linea is None:
            raise ValueError("El producto no esta en el pedido")
        self._productos.remove(linea)

    # ---- Calculos ----

    # Subtotal: suma el subtotal de cada linea (sin if por tipo de producto)
    def calcular_sub(self):
        total = 0
        for linea in self._productos:
            total = total + linea.calcular_sub()
        return round(total, 2)

    # Total de platos del pedido (incluye los de dentro de combos). Se usa para los envases
    def contar_platos(self):
        cantidad = 0
        for linea in self._productos:
            cantidad = cantidad + linea.contar_platos()
        return cantidad

    # METODO ABSTRACTO: cada tipo de pedido calcula su cargo adicional
    # (Local: 0, Llevar: envases, Delivery: envio)
    @abstractmethod
    def calcular_recargo(self):
        pass

    # Total = subtotal + recargo. El recargo lo resuelve la subclase (polimorfismo)
    def calcular_total(self):
        return round(self.calcular_sub() + self.calcular_recargo(), 2)

    # ---- Estados ----

    # Cambia el estado si la transicion es valida; si no, lanza error
    def cambiar_estado(self, nuevo, momento=None):
        if nuevo not in Pedido.TRANSICIONES[self._estado]:
            raise ValueError(f"Cambio de estado invalido: {self._estado} -> {nuevo}")
        # Antes de pasar a En preparacion se hacen validaciones extra
        if nuevo == Pedido.EN_PREPARACION:
            self._validar_para_preparar()
        self._estado = nuevo
        # Gancho: las subclases pueden reaccionar al cambio (Local libera la mesa, Delivery guarda la hora)
        self._al_cambiar_estado(nuevo, momento or datetime.now())

    # Cancelar es un cambio de estado a Cancelado (solo vale desde Registrado)
    def cancelar(self):
        self.cambiar_estado(Pedido.CANCELADO)

    # Validacion antes de preparar: el pedido no puede estar vacio.
    # Delivery la amplia para revisar el pedido minimo
    def _validar_para_preparar(self):
        if len(self._productos) == 0:
            raise ValueError("No se puede preparar un pedido sin productos")

    # Por defecto no hace nada; Local y Delivery la sobrescriben
    def _al_cambiar_estado(self, nuevo, momento):
        pass

    # ---- Detalle ----

    # Arma el texto con items, subtotal, cargos y total
    def mostrar_detalle(self):
        lineas = [f"Pedido {self._id_pedido} - {type(self).__name__} - {self._estado}"]
        for linea in self._productos:
            lineas.append("  " + linea.descripcion())
        lineas.append(f"Subtotal: Bs {self.calcular_sub():.2f}")
        lineas.append(f"{self.ETIQUETA_RECARGO}: Bs {self.calcular_recargo():.2f}")
        lineas.append(f"TOTAL: Bs {self.calcular_total():.2f}")
        return "\n".join(lineas)