# =====================================================
# Tarjeta.py  -  HIJA de Pago
# Comisión del 3 % a cargo del cliente.
# OJO: el delivery NO acepta tarjeta (regla 7).
# =====================================================

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

    # Total del pedido + la comisión
    def calcular_con_comision_total(self):
        total_pedido = self._redondear(self.pedido.calcular_total())
        return self._redondear(total_pedido + self.calcular_comision())

    # Reescribimos el método del padre: con tarjeta se paga el total CON comisión.
    # (Así Validar_pago() del padre ya funciona bien para la tarjeta)
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

    # Registra el pago y muestra el comprobante
    def registrar_pago(self):
        self._verificar_no_registrado()           # No cobrar dos veces
        # Le preguntamos al pedido si acepta tarjeta.
        # Si el pedido no tiene ese dato, se asume que sí acepta.
        # (El Delivery de tu compañero debe tener acepta_tarjeta = False)
        if not getattr(self.pedido, "acepta_tarjeta", True):
            raise ValueError("El delivery solo acepta efectivo o QR")
        if not self.Validar_pago():
            raise ValueError("El monto no cubre el total con comisión")
        self._marcar_registrado()
        print(self.generar_comprobante())