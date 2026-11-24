# =====================================================
# Efectivo.py  -  HIJA de Pago
# El cliente paga con billetes: se calcula el cambio.
# =====================================================

from decimal import Decimal
from Pago import Pago            # Traemos la clase padre


class Efectivo(Pago):

    def __init__(self, pedido, monto):
        super().__init__(pedido, monto)   # El padre guarda pedido, monto y fecha
        self._cambio = Decimal("0.00")    # Atributo propio: el cambio empieza en 0
    @property
    def cambio(self):
        return self._cambio

    # Revisa que el monto sea mayor a 0 y alcance para cubrir el total
    def validar_monto(self, monto):
        monto = Decimal(str(monto))
        return monto > 0 and monto >= self.calcular_pago_total()

    # Cambio = lo que dio el cliente - lo que debe
    def calcular_cambio(self):
        self._cambio = self._redondear(self.monto - self.calcular_pago_total())
        return self._cambio

    # Devuelve el comprobante como texto (no imprime, solo devuelve)
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

    # Registra el pago y muestra el comprobante
    def registrar_pago(self):
        self._verificar_no_registrado()           # No cobrar dos veces
        if not self.validar_monto(self.monto):
            raise ValueError("El monto recibido no cubre el total del pedido")
        self._marcar_registrado()
        print(self.generar_comprobante())