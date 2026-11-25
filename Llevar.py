from Pedido import Pedido


# Llevar: pedido para llevar. Cobra un envase por cada plato.
class Llevar(Pedido):
    def __init__(self, id_pedido, cliente, fecha=None):
        super().__init__(id_pedido, cliente, fecha)
        # MODIFICAR AQUI si cambia el costo del envase
        self._bs_adicional = 2.0
        self._cant_envases = 0

    @property
    def bs_adicional(self):
        return self._bs_adicional

    @property
    def cant_envases(self):
        return self._cant_envases

    # Envases = platos del pedido (incluye los de dentro de combos)
    # MODIFICAR AQUI si se cobra por producto o las bebidas no cuentan
    def calcular_costo_envase(self):
        self._cant_envases = self.contar_platos()
        return round(self._cant_envases * self._bs_adicional, 2)

    def calcular_recargo(self):
        return self.calcular_costo_envase()