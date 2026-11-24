
from decimal import Decimal
from Pago import Pago


class Tarjeta(Pago):

    def __init__(self, pedido, monto):
        super().__init__(pedido, monto)
        self._Comision = Decimal("0.03")      # 0.03 = 3 %

    @property
    def Comision(self):
        return self._Comision

    # La comisión es el 3 % del total del pedido
    def calcular_comision(self):
        total_pedido = self._redondear(self.pedido.calcular_total())
        return self._redondear(total_pedido * self._Comision)


    def calcular_con_comision_total(self):
        total_pedido = self._redondear(self.pedido.calcular_total())
        return self._redondear(total_pedido + self.calcular_comision())

    def calcular_pago_total(self):
        return self.calcular_con_comision_total()

    # Devuelve el comprobante como texto
    def generar_comprobante(self):
        return (
            "========== COMPROBANTE ==========\n"
            "Método de pago: TARJETA\n"
            f"Fecha: {self.fecha}\n"
            f"Comisión (3 %): Bs {self.calcular_comision()}\n"
            f"Total con comisión: Bs {self.calcular_pago_total()}\n"
            "================================="
        )


    def registrar_pago(self):
        self._verificar_no_registrado()           # No cobrar dos veces

        if not getattr(self.pedido, "acepta_tarjeta", True):
            raise ValueError("El delivery solo acepta efectivo o QR")
        if not self.Validar_pago():
            raise ValueError("El monto no cubre el total con comisión")
        self._marcar_registrado()
        print(self.generar_comprobante())