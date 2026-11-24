

from abc import ABC, abstractmethod          # ABC = clase abstracta
from decimal import Decimal, ROUND_HALF_UP   # Decimal: dinero sin errores
from datetime import date                    # Fecha del pago
class Pago(ABC):
    """Molde de todos los pagos. No se puede crear un Pago directamente."""
    def __init__(self, pedido, monto):
        # El guion bajo _ significa "protegido": no se toca desde afuera.
        # Para leerlos usamos las @property de más abajo.
        self._pedido = pedido              # Objeto Pedido que se paga (de tu compañero)
        self._monto = None                 # Se llena con el setter (que valida)
        self.monto = monto                 # Usa el setter (valida que sea > 0)
        self._fecha = date.today()         # Fecha de hoy
        self._registrado = False           # Todavía no se ha registrado el pago

    # ---------- PROPIEDADES (para leer los atributos protegidos) ----------
    @property
    def pedido(self):
        return self._pedido

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, valor):
        valor = Decimal(str(valor))        # Convertimos a Decimal
        if valor <= 0:                     # Validación: el monto debe ser mayor a 0
            raise ValueError("El monto debe ser mayor a 0")
        self._monto = valor

    @property
    def fecha(self):
        return self._fecha

    @property
    def registrado(self):
        return self._registrado           

    @staticmethod
    def _redondear(valor):
        return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


    def calcular_pago_total(self):
        return self._redondear(self._pedido.calcular_total())

  
    def Validar_pago(self):
        return self._monto >= self.calcular_pago_total()

    # Evita cobrar dos veces el mismo pago
    def _verificar_no_registrado(self):
        if self._registrado:
            raise ValueError("Este pago ya fue registrado")


    def _marcar_registrado(self):
        self._registrado = True

   
    @abstractmethod
    def generar_comprobante(self):
        pass

    @abstractmethod
    def registrar_pago(self):
        pass