# Cliente: datos de quien hace el pedido. Puede tener varios pedidos.
class Cliente:
    def __init__(self, nombre, telefono, direccion=""):
        self.nombre = nombre        # pasan por su setter (se validan)
        self.telefono = telefono
        self._direccion = str(direccion).strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if str(valor).strip() == "":
            raise ValueError("El nombre del cliente no puede estar vacio")
        self._nombre = str(valor).strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        if not self.verifica_telefono(valor):
            raise ValueError("El telefono debe tener 8 digitos y empezar con 6 o 7")
        self._telefono = valor

    @property
    def direccion(self):
        return self._direccion

    # Solo digitos, largo 8 y empieza con 6 o 7
    # MODIFICAR AQUI si cambia la regla del telefono
    def verifica_telefono(self, telefono=None):
        if telefono is None:
            telefono = self._telefono
        return telefono.isdigit() and len(telefono) == 8 and telefono[0] in "67"

    def mostrar_info_cliente(self):
        texto = f"Cliente: {self._nombre} - Telefono: {self._telefono}"
        if self._direccion != "":
            texto = texto + f" - Direccion: {self._direccion}"
        return texto