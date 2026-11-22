from Pedido import Pedido


# Llevar: pedido para llevar. Cobra un envase por cada plato.
class Llevar(Pedido):
    def __init__(self, id_pedido, cliente, fecha=None):
        super().__init__(id_pedido, cliente, fecha)
        # Costo de cada envase en Bs
        # MODIFICAR AQUI si cambia el costo del envase
        self._bs_adicional = 2

    @property
    def bs_adicional(self):
        return self._bs_adicional

    # Cantidad de envases = cantidad de platos
    # MODIFICAR AQUI si se cobra por producto o las bebidas no cuentan
    @property
    def con_envases(self):
        return self.contar_platos()

    # Costo de los envases = envases x costo de cada uno
    def calcular_costo_envase(self):
        return round(self.con_envases * self._bs_adicional, 2)

    # El cargo extra son los envases
    def calcular_recargo(self):
        return self.calcular_costo_envase()