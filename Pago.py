

from abc import ABC, abstractmethod          # ABC = clase abstracta
from decimal import Decimal, ROUND_HALF_UP   # Decimal: dinero sin errores
from datetime import date                    # Fecha del pago
class Pago(ABC):
    """Molde de todos los pagos. No se puede crear un Pago directamente."""
    def __init__(self, pedido, monto):
        # El doble guion bajo __ significa "privado": solo se toca dentro de Pago.
        # Para leerlos desde las clases hijas o desde afuera usamos los @property.
        self.__pedido = pedido             # Objeto Pedido que se paga
        self.__monto = None                # Se llena con el setter (que valida)
        self.monto = monto                 # Usa el setter (valida que sea > 0)
        self.__fecha = date.today()        # Fecha de hoy
        self.__registrado = False          # Todavía no se ha registrado el pago
    # ---------- PROPIEDADES (para leer los atributos privados) ----------
    @property
    def pedido(self):
        return self.__pedido
    @property
    def monto(self):
        return self.__monto
    @monto.setter
    def monto(self, valor):
        valor = Decimal(str(valor))        # Convertimos a Decimal
        if valor <= 0:                     # Validación: el monto debe ser mayor a 0
            raise ValueError("El monto debe ser mayor a 0")
        self.__monto = valor

    @property
    def fecha(self):
        return self.__fecha

    @property
    def registrado(self):
        return self.__registrado           # True si el pago ya se registró

    # ---------- MÉTODOS ----------
    # Redondea a 2 decimales (todos los montos del proyecto van así)
    @staticmethod
    def _redondear(valor):
        return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Cuánto hay que pagar en total. Se lo pide al Pedido.
    def calcular_pago_total(self):
        return self._redondear(self.__pedido.calcular_total())

    # Revisa que el monto alcance para pagar
    def Validar_pago(self):
        return self.__monto >= self.calcular_pago_total()

    # Evita cobrar dos veces el mismo pago
    def _verificar_no_registrado(self):
        if self.__registrado:
            raise ValueError("Este pago ya fue registrado")

    # Marca el pago como registrado (lo llaman las hijas al terminar)
    def _marcar_registrado(self):
        self.__registrado = True

    # Métodos abstractos: cada hija DEBE escribir los suyos
    @abstractmethod
    def generar_comprobante(self):
        pass

    @abstractmethod
    def registrar_pago(self):
        pass