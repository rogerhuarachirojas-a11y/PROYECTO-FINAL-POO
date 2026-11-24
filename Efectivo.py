

from decimal import Decimal
from Pago import Pago            # Traemos la clase padre
class Efectivo(Pago):

    def __init__(self, pedido, monto):
        super().__init__(pedido, monto)   # El padre guarda pedido, monto y fecha
        self._cambio = Decimal("0.00")    # Atributo propio: el cambio empieza en 0
    @property
    def cambio(self):
        return self._cambio

    def validar_monto(self, monto):
        monto = Decimal(str(monto))
        return monto > 0 and monto >= self.calcular_pago_total()


    def calcular_cambio(self):
        self._cambio = self._redondear(self.monto - self.calcular_pago_total())
        return self._cambio

    def generar_comprobante(self):
        self.calcular_cambio()
        return (
            "========== COMPROBANTE ==========\n"
            "Método de pago: EFECTIVO\n"
            f"Fecha: {self.fecha}\n"
            f"Total a pagar: Bs {self.calcular_pago_total()}\n"
            f"Monto recibido: Bs {self.monto}\n"
            f"Cambio: Bs {self.cambio}\n"
            "================================="
        )

    def registrar_pago(self):
        self._verificar_no_registrado()           # No cobrar dos veces
        if not self.validar_monto(self.monto):
            raise ValueError("El monto recibido no cubre el total del pedido")
        self._marcar_registrado()
        print(self.generar_comprobante())