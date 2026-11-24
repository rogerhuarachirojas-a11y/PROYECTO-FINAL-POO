from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Producto tiene un Combo (diagrama), pero Combo tambien usa Producto.
# Para no crear un import circular, Combo se importa solo para los tipos.
if TYPE_CHECKING:
    from Combo import Combo


# Producto: clase ABSTRACTA (hereda de ABC y tiene un @abstractmethod).
# No se puede crear un Producto directo; hay que usar Plato o Bebida.
class Producto(ABC):
    TODOS_LOS_DIAS = "Todos los dias"

    def __init__(self, nombre, precio, disponible=TODOS_LOS_DIAS, menu=None):
        if not nombre:
            raise ValueError("El producto necesita un nombre")
        if not Producto.verificar_precio(precio):
            raise ValueError("El precio debe ser un numero mayor a 0")
        self._nombre = nombre
        self._precio = float(precio)
        self._disponible = disponible            # texto que describe cuando se sirve
        self._menu = list(menu) if menu else []  # menus donde aparece el producto
        self._combo: Combo | None = None         # combo al que pertenece (si tiene)

    # ---- Propiedades ----
    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def disponible(self):
        return self._disponible

    # Devuelve una COPIA (tupla): desde fuera no se puede modificar la lista del menu
    @property
    def menu(self):
        return tuple(self._menu)

    @property
    def combo(self):
        return self._combo

    # Lo usa Combo.agregar_producto para enlazar el producto con su combo
    @combo.setter
    def combo(self, combo: Combo | None):
        self._combo = combo

    # ---- Validaciones ----

    # Un precio es valido si es un numero mayor a 0
    @staticmethod
    def verificar_precio(precio):
        return isinstance(precio, (int, float)) and precio > 0

    # ---- Disponibilidad ----

    # Por defecto el producto se sirve todos los dias; Plato la sobrescribe.
    # Pedido la llama con el nombre del dia (lunes, martes, ...)
    def esta_disponible(self, dia):
        return True

    # Cuantos platos cuenta este producto (se usa para los envases).
    # Por defecto 0; Plato devuelve 1 y Combo suma los de sus productos
    def contar_platos(self):
        return 0

    # ---- Calculos ----

    # METODO ABSTRACTO: cada producto calcula su precio (Plato: fijo, Bebida: segun tamano)
    @abstractmethod
    def calcular_precio(self):
        pass