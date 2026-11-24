<<<<<<< HEAD
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
=======
# ProductoPedido: una linea del pedido (producto + cantidad). Ejemplo: "2 x Silpancho".
class ProductoPedido:
    def __init__(self, producto, cantidad):
        self._producto = producto
        self._precio_unitario = round(producto.calcular_precio(), 2)  # precio al agregarlo
        self._cantidad = cantidad
        if not self.validar_cantidad():
            raise ValueError("La cantidad debe ser un entero entre 1 y 20")

    # True si la cantidad es un entero de 1 a 20 (sin parametro revisa la cantidad actual)
    # MODIFICAR AQUI si cambia el limite
    def validar_cantidad(self, cantidad=None):
        if cantidad is None:
            cantidad = self._cantidad
        return isinstance(cantidad, int) and 1 <= cantidad <= 20

    @property
    def producto(self):
        return self._producto

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if not self.validar_cantidad(valor):
            raise ValueError("La cantidad debe ser un entero entre 1 y 20")
        self._cantidad = valor

    def calcular_sub(self):
        return round(self._precio_unitario * self._cantidad, 2)

    # Platos de la linea (si es un combo, cuenta los platos de adentro)
    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad
>>>>>>> 59a2e2b947858ef0df31b82b64850bef6749560e
