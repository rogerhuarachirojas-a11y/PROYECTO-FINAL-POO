from datetime import datetime

from Pedido import Pedido


# Delivery: pedido a domicilio. Cobra envio segun la zona.
class Delivery(Pedido):
    # MODIFICAR AQUI para agregar una zona, por ejemplo "Tiquipaya": 18
    ZONAS = {"Cercado": 8, "Quillacollo": 15, "Sacaba": 15, "Vinto": 20}

    def __init__(self, id_pedido, cliente, zona, direccion_entrega, fecha=None):
        super().__init__(id_pedido, cliente, fecha)
        zona = str(zona).strip().capitalize()
        if zona not in Delivery.ZONAS:
            raise ValueError(f"Zona no valida: {zona}")
        if str(direccion_entrega).strip() == "":
            raise ValueError("La direccion de entrega no puede estar vacia")
        self._zona = zona
        self._direccion_entrega = str(direccion_entrega).strip()
        self._tiempo_duracion = 0   # minutos entre el registro y la entrega

    @property
    def zona(self):
        return self._zona

    @property
    def direccion_entrega(self):
        return self._direccion_entrega

    @property
    def tiempo_duracion(self):
        return self._tiempo_duracion

    # Gratis en Cercado desde Bs 150; si no, el precio de la zona
    # MODIFICAR AQUI si cambia el monto o la zona del envio gratis
    def calcular_envio_deli(self):
        if self._zona == "Cercado" and self.calcular_sub() >= 150:
            return 0
        return Delivery.ZONAS[self._zona]

    def calcular_recargo(self):
        return self.calcular_envio_deli()

    # MODIFICAR AQUI si cambia el pedido minimo
    def validar_pedido_min(self):
        return self.calcular_sub() >= 40

    # Antes de preparar se revisa el minimo; al entregar se guarda cuantos minutos tardo.
    # El parametro hora solo sirve para probar (por defecto es la hora actual).
    def cambiar_estado(self, est, hora=None):
        if est == Pedido.EN_PREPARACION and not self.validar_pedido_min():
            raise ValueError("El pedido minimo para delivery es Bs 40")
        super().cambiar_estado(est)
        if est == Pedido.ENTREGADO:
            hora = hora or datetime.now()
            segundos = (hora - self._fecha).total_seconds()
            self._tiempo_duracion = int(segundos // 60)

    # Retraso = mas de 60 minutos; la compensacion es devolver el envio
    # MODIFICAR AQUI si cambia el limite o la compensacion
    def calcular_compensacion(self):
        if self._tiempo_duracion > 60:
            return self.calcular_envio_deli()
        return 0