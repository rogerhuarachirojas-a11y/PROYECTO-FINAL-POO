from Producto import Producto


class Plato(Producto):
    DIAS = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")

    # Si no se indican dias, el plato se sirve todos los dias
    def __init__(self, nombre, precio, dias_disponibles=None, menu=None):
        if dias_disponibles:
            dias = [d.lower() for d in dias_disponibles]
        else:
            dias = list(Plato.DIAS)
        for dia in dias:
            if dia not in Plato.DIAS:
                raise ValueError(f"Dia invalido: {dia} (use {', '.join(Plato.DIAS)})")
        super().__init__(nombre, precio, ", ".join(dias), menu)
        self._dias_disponibles = dias

    @property
    def dias_disponibles(self):
        return tuple(self._dias_disponibles)


    def esta_disponible(self, dia):
        return dia.lower() in self._dias_disponibles

    # Un plato cuenta como 1 plato
    def contar_platos(self):
        return 1

    def calcular_precio(self):
        return round(self._precio, 2)