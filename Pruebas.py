# Archivo principal de pruebas. Se ejecuta con:  python pruebas.py
# Corre las pruebas de productos, las de pedidos y los escenarios completos de abajo.
from datetime import date, datetime, timedelta

import pruebas_productos
import pruebas_pedidos
import pruebas_pagos

from Producto import Producto
from Plato import Plato
from Bebida import Bebida
from Combo import Combo
from Cliente import Cliente
from Pedido import Pedido
from Local import Local
from Llevar import Llevar
from Delivery import Delivery
from Restaurante import Restaurante
from Efectivo import Efectivo
from PagoEnQR import PagoEnQR
from Tarjeta import Tarjeta

LUNES = datetime(2026, 11, 16, 12, 0)


def crear_menu():
    silpancho = Plato("Silpancho", 35)
    mocochinchi = Bebida("Mocochinchi", 6, "vaso", "natural")
    combo = Combo("Combo 1", [silpancho, mocochinchi])
    return silpancho, mocochinchi, combo


# ---------- Escenarios completos (todas las clases juntas) ----------

# Flujo completo de un delivery: cliente, combos, estados, entrega y compensacion
def prueba_flujo_delivery_completo():
    silpancho, mocochinchi, combo = crear_menu()
    cliente = Cliente("Ana Rojas", "71234567", "Av. Blanco Galindo")
    p = Delivery("D1", cliente, "Quillacollo", cliente.direccion, LUNES)
    p.agregar_pro(combo, 2)
    assert p.calcular_total() == 88.80          # caso de referencia (reglas base)
    p.cambiar_estado(Pedido.EN_PREPARACION)
    p.cambiar_estado(Pedido.LISTO)
    p.cambiar_estado(Pedido.ENTREGADO, LUNES + timedelta(minutes=45))
    assert p.calcular_compensacion() == 0       # llego a tiempo

    q = Delivery("D2", cliente, "Quillacollo", cliente.direccion, LUNES)
    q.agregar_pro(combo, 2)
    q.cambiar_estado(Pedido.EN_PREPARACION)
    q.cambiar_estado(Pedido.LISTO)
    q.cambiar_estado(Pedido.ENTREGADO, LUNES + timedelta(minutes=90))
    assert q.calcular_compensacion() == 15      # llego tarde: se devuelve el envio

# Pedido local con combo dentro de combo; la mesa se libera al entregar
def prueba_flujo_local_con_combo_anidado():
    silpancho, mocochinchi, combo = crear_menu()
    cliente = Cliente("Luis Vera", "61234567")
    Local._mesas_ocupadas.clear()
    grande = Combo("Grande", [combo, Plato("Pique macho", 45)])
    p = Local("L1", cliente, 5, LUNES)
    p.agregar_pro(grande)
    assert p.calcular_total() == 73.71          # (36.90 + 45) x 0.90, sin cargos
    p.cambiar_estado(Pedido.EN_PREPARACION)
    p.cambiar_estado(Pedido.LISTO)
    p.cambiar_estado(Pedido.ENTREGADO)
    Local("L2", cliente, 5, LUNES)              # la mesa 5 ya esta libre

# Para llevar: los envases cuentan los platos de dentro del combo, no las bebidas
def prueba_flujo_llevar_envases_en_combo():
    silpancho, mocochinchi, combo = crear_menu()
    cliente = Cliente("Eva Soto", "78765432")
    p = Llevar("LL1", cliente, fecha=LUNES)
    p.agregar_pro(combo, 3)
    p.agregar_pro(mocochinchi, 2)
    assert p.contar_platos() == 3
    assert p.calcular_recargo() == 6.0
    assert p.calcular_total() == round(3 * 36.90 + 2 * 6 + 6, 2)

# Polimorfismo: un mismo codigo calcula el total de los tres tipos de pedido
def prueba_polimorfismo_tres_tipos():
    silpancho, mocochinchi, combo = crear_menu()
    cliente = Cliente("Ana Rojas", "71234567")
    Local._mesas_ocupadas.clear()
    pedidos = [Local("A", cliente, 7, LUNES),
               Llevar("B", cliente, fecha=LUNES),
               Delivery("C", cliente, "Vinto", "Calle 5", LUNES)]
    for p in pedidos:
        p.agregar_pro(silpancho, 2)             # subtotal 70
    totales = [p.calcular_total() for p in pedidos]
    assert totales == [70, 74, 90]              # local, 70 + 2 envases, 70 + envio 20

# Cambio en vivo: agregar un Postre sin tocar Pedido ni Combo
def prueba_postre_nuevo_sin_tocar_pedido():
    class Postre(Producto):
        def __init__(self, nombre, precio, crema=False):
            super().__init__(nombre, precio)
            self._crema = crema
        def calcular_precio(self):
            return self._precio + 3 if self._crema else self._precio
        def disponible(self, dia):
            return True
        def contar_platos(self):
            return 0
    silpancho, mocochinchi, combo = crear_menu()
    helado = Postre("Helado", 10, True)         # 10 + 3 de crema = 13
    cliente = Cliente("Ana Rojas", "71234567")
    p = Llevar("P1", cliente, fecha=LUNES)
    p.agregar_pro(helado)
    assert p.calcular_sub() == 13
    assert p.calcular_recargo() == 0            # el postre no lleva envase
    nuevo = Combo("Con postre", [silpancho, helado])
    assert nuevo.calcular_precio() == round((35 + 13) * 0.9, 2)

# Cambio en vivo: una zona nueva de delivery se agrega solo con un dato
def prueba_zona_nueva_tiquipaya():
    silpancho, mocochinchi, combo = crear_menu()
    cliente = Cliente("Ana Rojas", "71234567")
    Delivery.ZONAS["Tiquipaya"] = 18
    try:
        p = Delivery("T1", cliente, "Tiquipaya", "Calle 9", LUNES)
        p.agregar_pro(silpancho, 2)
        assert p.calcular_total() == 88
    finally:
        del Delivery.ZONAS["Tiquipaya"]         # se deja como estaba


# Restaurante: crear pedido, cobrar con comprobante y no cobrar dos veces
def prueba_restaurante_cobro_y_doble_cobro():
    rest = Restaurante()
    silpancho, mocochinchi, combo = crear_menu()
    rest.registrar_producto(silpancho)
    rest.registrar_producto(mocochinchi)
    rest.armar_combo("Combo 1", [silpancho, mocochinchi])
    ana = rest.registrar_cliente("Ana Rojas", "71234567", "Calle 1")
    p = rest.crear_pedido_delivery(ana, "Quillacollo", "Calle 1")
    p.agregar_pro(rest.productos[2], 2)          # el combo armado
    comprobante = rest.cobrar_pedido(Efectivo(p, 100))
    assert "88.80" in comprobante and "P001" in comprobante
    try:
        rest.cobrar_pedido(Efectivo(p, 100))
        assert False
    except ValueError:
        pass

# Restaurante: menu disponible por dia (el chicharron solo los domingos)
def prueba_restaurante_menu_por_dia():
    rest = Restaurante()
    silpancho, mocochinchi, combo = crear_menu()
    chicharron = Plato("Chicharron", 50, ["domingo"])
    rest.registrar_producto(silpancho)
    rest.registrar_producto(chicharron)
    rest.armar_combo("Combo Domingo", [chicharron, mocochinchi])
    lunes = rest.listar_menu_disponible("lunes")
    domingo = rest.listar_menu_disponible("domingo")
    assert len(lunes) == 1 and len(domingo) == 3

# Restaurante: reporte de ventas del dia por tipo y los 3 productos mas vendidos
def prueba_restaurante_reporte_del_dia():
    rest = Restaurante()
    silpancho, mocochinchi, combo = crear_menu()
    pique = Plato("Pique macho", 45)
    sopa = Plato("Sopa de mani", 30)
    ana = rest.registrar_cliente("Ana Rojas", "71234567", "Calle 1")
    Local._mesas_ocupadas.clear()
    local = rest.crear_pedido_local(ana, 4)
    local.agregar_pro(silpancho, 3)
    local.agregar_pro(sopa, 1)
    rest.cobrar_pedido(Efectivo(local, 500))
    llevar = rest.crear_pedido_llevar(ana)
    llevar.agregar_pro(silpancho, 1)
    llevar.agregar_pro(pique, 2)
    llevar.agregar_pro(mocochinchi, 1)
    rest.cobrar_pedido(Tarjeta(llevar))
    pendiente = rest.crear_pedido_llevar(ana)    # sin cobrar: no entra al reporte
    pendiente.agregar_pro(sopa, 5)
    reporte = rest.reporte_ventas_dia(date.today())
    assert reporte["Local"] == [1, 135]          # 3 x 35 + 30
    assert reporte["Llevar"] == [1, 137]         # 35 + 90 + 6 + 3 platos x Bs 2 de envase
    top = rest.productos_mas_vendidos(date.today(), 3)
    assert top == [("Silpancho", 4), ("Pique macho", 2), ("Sopa de mani", 1)]


# ---------- Ejecucion de todo ----------
def correr(modulo, nombre):
    ok, fallos = 0, 0
    funciones = [(n, f) for n, f in sorted(vars(modulo).items()) if n.startswith("prueba_")]
    print(f"\n== {nombre} ==")
    for n, f in funciones:
        try:
            f()
            print("  OK    ", n)
            ok += 1
        except Exception as e:
            print("  FALLO ", n, "->", type(e).__name__, e)
            fallos += 1
    return ok, fallos


if __name__ == "__main__":
    import sys
    total_ok, total_fallos = 0, 0
    for mod, nombre in [(pruebas_productos, "Productos"), (pruebas_pedidos, "Pedidos"), (pruebas_pagos, "Pagos"), (sys.modules[__name__], "Escenarios completos")]:
        ok, fallos = correr(mod, nombre)
        total_ok += ok
        total_fallos += fallos
    print(f"\nResultado: {total_ok} pruebas pasaron, {total_fallos} fallaron")