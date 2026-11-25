from datetime import datetime, timedelta

from Bebida import Bebida
from Cliente import Cliente
from Combo import Combo
from Delivery import Delivery
from DetalleComboPedido import DetalleComboPedido
from Efectivo import Efectivo
from Llevar import Llevar
from Local import Local
from PagoEnQr import PagoEnQR
from Pedido import Pedido
from Plato import Plato
from Producto import Producto
from Tarjeta import Tarjeta


def main():
    print("=== SISTEMA DE PEDIDOS SABOR VALLUNO ===\n")

    # 1. Cliente
    cliente = Cliente("Carlos Mamani", "71234567", "Av. Blanco Galindo km 10")
    print(cliente.mostrar_info_cliente(), "\n")

    # 2. Productos (Plato, Bebida con precio jarra y vaso, y Combo)
    silpancho = Plato("Silpancho Cochabambino", 35.0)
    pique = Plato("Pique Macho", 55.0)
    chicha = Bebida("Chicha Morada", precio=15.0, precio_vaso=5.0, tamano="Jarra", tipo="Natural")
    gaseosa = Bebida("Coca Cola", precio=12.0, precio_vaso=6.0, tamano="Vaso", tipo="Gaseosa")

    combo_valluno = Combo("Combo Valluno Familiar", [silpancho, pique, chicha])
    print(f"Combo: {combo_valluno.nombre} | Precio con 10% desc.: Bs {combo_valluno.calcular_precio()} | Platos: {combo_valluno.contar_platos()}\n")

    # 3. Pedido LOCAL + Pago con TARJETA (3% de comision)
    p_local = Local("PED-001", cliente, mesa=4)
    p_local.agregar_pro(silpancho, 2)
    p_local.agregar_pro(gaseosa, 2)
    print(f"[LOCAL] Subtotal: Bs {p_local.calcular_sub()} | Recargo: Bs {p_local.calcular_recargo()} | Total: Bs {p_local.calcular_total()}")

    p_local.cambiar_estado(Pedido.EN_PREPARACION)
    p_local.cambiar_estado(Pedido.LISTO)
    p_local.cambiar_estado(Pedido.ENTREGADO)

    pago_tarjeta = Tarjeta(p_local, 100)
    pago_tarjeta.registrar_pago()
    print()

    # 4. Pedido PARA LLEVAR + Pago en EFECTIVO (Bs 2 por cada plato, incluye platos dentro de combos)
    p_llevar = Llevar("PED-002", cliente)
    p_llevar.agregar_pro(combo_valluno, 1)  # 2 platos dentro del combo = 2 envases (Bs 4.0)
    p_llevar.agregar_pro(gaseosa, 1)        # 0 envases
    recargo_llevar = p_llevar.calcular_recargo()
    print(f"[LLEVAR] Subtotal: Bs {p_llevar.calcular_sub()} | Envases ({p_llevar.cant_envases}): Bs {recargo_llevar} | Total: Bs {p_llevar.calcular_total()}")

    pago_efectivo = Efectivo(p_llevar, 120)
    pago_efectivo.registrar_pago()
    print()

    # 5. Pedido DELIVERY + Pago en QR (Quillacollo = Bs 15 envio, minimo Bs 40)
    hora_inicio = datetime.now() - timedelta(minutes=75)
    p_delivery = Delivery("PED-003", cliente, "Quillacollo", "Plaza Bolivar #12", fecha=hora_inicio)
    p_delivery.agregar_pro(pique, 1)
    print(f"[DELIVERY] Subtotal: Bs {p_delivery.calcular_sub()} | Envio ({p_delivery.zona}): Bs {p_delivery.calcular_recargo()} | Total: Bs {p_delivery.calcular_total()}")

    p_delivery.cambiar_estado(Pedido.EN_PREPARACION)
    p_delivery.cambiar_estado(Pedido.LISTO)
    p_delivery.cambiar_estado(Pedido.ENTREGADO, hora=datetime.now())
    print(f"[DELIVERY] Tiempo entrega: {p_delivery.tiempo_duracion} min | Compensacion por retraso: Bs {p_delivery.calcular_compensacion()}")

    pago_qr = PagoEnQR(p_delivery, 70, "1234567890")
    pago_qr.registrar_pago()

    # 6. Verificar bloqueo de tarjeta en Delivery
    try:
        Tarjeta(p_delivery, 100).registrar_pago()
    except ValueError as e:
        print(f"\n[VALIDACION OK] Delivery con tarjeta bloqueado: {e}")


if __name__ == "__main__":
    main()

