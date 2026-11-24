
from Pago import Pago


class PagoEnQR(Pago):

    # Lista privada COMPARTIDA por todos los pagos QR: guarda los códigos ya usados
    __codigos_usados = set()

    def __init__(self, pedido, monto, Codigo_transQR):
        super().__init__(pedido, monto)
        self.__Codigo_transQR = str(Codigo_transQR)   # Atributo privado

    @property
    def Codigo_transQR(self):
        return self.__Codigo_transQR

    # El código es válido si tiene SOLO números y exactamente 10 dígitos
    def validar_cod_transQR(self):
        return self.__Codigo_transQR.isdigit() and len(self.__Codigo_transQR) == 10

    # Devuelve el comprobante como texto
    def generar_comprobante(self):
        return (
            "========== COMPROBANTE ==========\n"
            "Método de pago: QR\n"
            f"Fecha: {self.fecha}\n"
            f"Código de transacción: {self.Codigo_transQR}\n"
            f"Total pagado: Bs {self.calcular_pago_total()}\n"
            "================================="
        )

    # Registra el pago y muestra el comprobante
    def registrar_pago(self):
        self._verificar_no_registrado()           # No cobrar dos veces
        if not self.validar_cod_transQR():
            raise ValueError("El código de transacción QR debe tener 10 dígitos")
        if self.__Codigo_transQR in PagoEnQR.__codigos_usados:
            raise ValueError("Ese código de transacción QR ya fue usado")
        if not self.Validar_pago():
            raise ValueError("El monto no cubre el total del pedido")
        PagoEnQR.__codigos_usados.add(self.__Codigo_transQR)   # Guardamos el código
        self._marcar_registrado()
        print(self.generar_comprobante())