from Pedido import Pedido


# Local: pedido para comer en el restaurante. Sin cargos; mesa del 1 al 15.
class Local(Pedido):
    # Mesas con un pedido abierto (compartida por todos los pedidos Local)
    _mesas_ocupadas = []

    def __init__(self, id_pedido, cliente, mesa, fecha=None):
        super().__init__(id_pedido, cliente, fecha)
        self._mesa = mesa
        if not self.validar_mesa():
            raise ValueError("La mesa debe ser un entero entre 1 y 15")
        if not self.verificar_pedidos_mesa():
            raise ValueError(f"La mesa {mesa} ya tiene un pedido abierto")
        Local._mesas_ocupadas.append(mesa)

    @property
    def mesa(self):
        return self._mesa

    # MODIFICAR AQUI si cambia la cantidad de mesas
    def validar_mesa(self):
        return isinstance(self._mesa, int) and 1 <= self._mesa <= 15

    # True si la mesa NO tiene otro pedido abierto
    def verificar_pedidos_mesa(self):
        return self._mesa not in Local._mesas_ocupadas

    # Al entregar o cancelar, la mesa queda libre
    def cambiar_estado(self, est):
        super().cambiar_estado(est)
        if est == Pedido.ENTREGADO or est == Pedido.CANCELADO:
            Local._mesas_ocupadas.remove(self._mesa)

    def calcular_recargo(self):
        return 0