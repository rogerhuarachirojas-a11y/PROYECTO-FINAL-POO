# Pruebas de Producto, Plato, Bebida y Combo. Se ejecuta con: python pruebas_productos.py
from Producto import Producto
from Plato import Plato
from Bebida import Bebida
from Combo import Combo

silpancho = Plato("Silpancho", 35)
mocochinchi = Bebida("Mocochinchi", 6, "vaso", "natural")


def lanza_error(accion):
    try:
        accion()
    except ValueError:
        return True
    return False


# Producto es abstracta: no se puede crear
def prueba_producto_abstracto():
    try:
        Producto("X", 10)
        assert False
    except TypeError:
        pass

# Precio mayor que cero y nombre no vacio
def prueba_validaciones():
    for precio in [0, -5, "10"]:
        assert lanza_error(lambda: Plato("Sopa", precio))
    assert lanza_error(lambda: Plato("  ", 10))

# La jarra cuesta 3 veces el vaso
def prueba_bebida_jarra():
    assert Bebida("Mocochinchi", 6, "jarra").calcular_precio() == 18
    assert mocochinchi.calcular_precio() == 6
    assert lanza_error(lambda: Bebida("Cola", 5, "botella"))
    assert mocochinchi.contar_platos() == 0

# El chicharron solo se vende los domingos
def prueba_plato_dias():
    chicharron = Plato("Chicharron", 50, ["domingo"])
    assert chicharron.disponible("domingo")
    assert not chicharron.disponible("lunes")
    assert silpancho.disponible("martes")
    assert chicharron.contar_platos() == 1

# Caso de referencia: (35 + 6) x 0.90 = 36.90
def prueba_combo_precio():
    assert Combo("Combo 1", [silpancho, mocochinchi]).calcular_precio() == 36.90

# Combo dentro de combo: (36.90 + 45) x 0.90 = 73.71
def prueba_combo_dentro_de_combo():
    combo = Combo("Combo 1", [silpancho, mocochinchi])
    grande = Combo("Grande", [combo, Plato("Pique macho", 45)])
    assert grande.calcular_precio() == 73.71
    assert grande.contar_platos() == 2

# Un combo necesita al menos 2 productos
def prueba_combo_minimo():
    assert lanza_error(lambda: Combo("Solo", [silpancho]))

# El combo esta disponible solo si todos sus productos lo estan
def prueba_combo_disponibilidad():
    combo = Combo("Domingo", [Plato("Chicharron", 50, ["domingo"]), mocochinchi])
    assert combo.disponible("domingo")
    assert not combo.disponible("lunes")

# productos es una copia (tupla)
def prueba_combo_productos_copia():
    combo = Combo("Combo 1", [silpancho, mocochinchi])
    assert isinstance(combo.productos, tuple) and len(combo.productos) == 2


if __name__ == "__main__":
    pruebas = [f for n, f in sorted(globals().items()) if n.startswith("prueba_")]
    for f in pruebas:
        f()
        print("OK ", f.__name__)
    print(f"\n{len(pruebas)} pruebas pasaron")