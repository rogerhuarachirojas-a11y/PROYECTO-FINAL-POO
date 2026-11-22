from Pedido import Pedido


# Local: pedido para comer en el restaurante. Sin cargos; necesita mesa del 1 al 15.
class Local(Pedido):
    # Mesas que tienen un pedido abierto (compartida por todos los pedidos Local)
    _mesas_ocupadas = []

    def __init__(self, id_pedido, cliente, mesa, fecha=None):
        super().__init__(id_pedido, cliente, fecha)
        self.validar_mesa(mesa)
        self._mesa = mesa
        self.verificar_pedidos_mesa()
        Local._mesas_ocupadas.append(mesa)

    @property
    def mesa(self):
        return self._mesa

    # La mesa debe ser un entero de 1 a 15
    # MODIFICAR AQUI si cambia la cantidad de mesas
    def validar_mesa(self, mesa):
        if not isinstance(mesa, int):
            raise ValueError("La mesa debe ser un numero entero")
        if mesa < 1 or mesa > 15:
            raise ValueError("La mesa debe estar entre 1 y 15")

    # Una mesa no puede tener dos pedidos abiertos
    def verificar_pedidos_mesa(self, mesa=None):
        if mesa is None:
            mesa = self._mesa
        if mesa in Local._mesas_ocupadas:
            raise ValueError(f"La mesa {mesa} ya tiene un pedido abierto")

    # Al entregar o cancelar, la mesa queda libre
    def cambiar_estado(self, nuevo):
        super().cambiar_estado(nuevo)
        if nuevo == Pedido.ENTREGADO or nuevo == Pedido.CANCELADO:
            Local._mesas_ocupadas.remove(self._mesa)

    # No hay cargo extra
    def calcular_recargo(self):
        return 0