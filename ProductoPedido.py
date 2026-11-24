from abc import ABC, abstractmethod
class Producto(ABC):
    TODOS_LOS_DIAS = "Todos los dias"

    def __init__(self, nombre, precio, disponible=TODOS_LOS_DIAS, menu=None):
        if not nombre:
            raise ValueError("El producto necesita un nombre")
        if not Producto.verificar_precio(precio):
            raise ValueError("El precio debe ser un numero mayor a 0")
        self._nombre = nombre
        self._precio = float(precio)
        self._disponible = disponible            
        self._menu = list(menu) if menu else []  
        self._combo = None                       

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

    @property
    def menu(self):
        return tuple(self._menu)

    @property
    def combo(self):
        return self._combo

    @combo.setter
    def combo(self, combo):
        self._combo = combo

    
    @staticmethod
    def verificar_precio(precio):
        return isinstance(precio, (int, float)) and precio > 0


    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0

    @abstractmethod
    def calcular_precio(self):
        pass