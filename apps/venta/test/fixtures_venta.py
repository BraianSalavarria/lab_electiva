from datetime import date, timedelta
from decimal import Decimal
import pytest
from apps.usuario.test.fixture_user import get_authenticated_client, api_client,get_user
from apps.producto.test.fixtures_categoria import get_categoria, get_categorias
from apps.producto.test.fixtures_producto import get_producto, get_productos
from apps.venta.models import ItemVenta, Venta


def create_venta(usuario):
    venta= Venta.objects.create(usuario=usuario,total=Decimal("0.00"))
    return venta

def create_item_venta(venta,producto, cantidad):
    item_venta= ItemVenta.objects.create(venta=venta, producto=producto, cantidad=cantidad)
    return item_venta

def create_venta_with_items(venta,items):
    for producto, cantidad in items:
        item_venta= create_item_venta(venta, producto, cantidad)
        venta.total += item_venta.subtotal
        producto.stock-=cantidad
    venta.save()
    return venta


@pytest.fixture
def get_venta_not_item(get_authenticated_client,get_user):
    user =get_user
    venta = create_venta(usuario=user)
    return venta


@pytest.fixture
def get_venta(get_venta_not_item, get_producto):
    venta = get_venta_not_item
    producto = get_producto
    item = create_item_venta(venta, producto, 5)
    venta.total = item.subtotal
    venta.save()
    return venta


@pytest.fixture
def get_item_venta(get_authenticated_client,get_venta_not_item,get_producto):
    venta = get_venta_not_item
    producto = get_producto
    item = create_item_venta(venta, producto, 5)
    return item


@pytest.fixture
def get_ventas_not_items(get_authenticated_client,get_user):
    user=get_user
    ventas=[]


    fecha_actual_mocker = date(2025, 7, 17)

    #creamos las ditintas ventas con fechas diferentes

    venta1=create_venta(usuario=user)
    venta1.fecha=fecha_actual_mocker
    venta1.save()
    ventas.append(venta1)

    venta2 = create_venta(usuario=user)
    venta2.fecha=fecha_actual_mocker
    venta2.save()
    ventas.append(venta2)

    venta3 = create_venta(usuario=user)
    venta3.fecha=fecha_actual_mocker - timedelta(days=1)
    venta3.save()
    ventas.append(venta3)

    venta4 = create_venta(usuario=user)
    venta4.fecha=fecha_actual_mocker - timedelta(days=3)
    venta4.save()
    ventas.append(venta4)

    venta5 = create_venta(usuario=user)
    venta5.fecha=fecha_actual_mocker - timedelta(days=3)
    venta5.save()
    ventas.append(venta5)

    venta6 = create_venta(usuario=user)
    venta6.fecha=fecha_actual_mocker - timedelta(days=2)
    venta6.save()
    ventas.append(venta6)

    venta7 = create_venta(usuario=user)
    venta7.fecha=fecha_actual_mocker - timedelta(days=4)
    venta7.save()
    ventas.append(venta7)

    venta8 = create_venta(usuario=user)
    venta8.fecha=fecha_actual_mocker - timedelta(days=4)
    venta8.save()
    ventas.append(venta8)

    venta9 = create_venta(usuario=user)
    venta9.fecha=fecha_actual_mocker
    venta9.save()
    ventas.append(venta9)

    venta10 = create_venta(usuario=user)
    venta10.fecha=fecha_actual_mocker
    venta10.save()
    ventas.append(venta10)

    return ventas


@pytest.fixture
def get_ventas(get_authenticated_client,get_productos,get_ventas_not_items,get_user):

    #lista de ventas completas
    ventas=[]
    #preparamos los productos
    producto1,producto2,producto3,producto4,producto5,producto6,producto7, *_ = get_productos
    #creamos los distintos items para las ventas para un usuario con permisos limitados

    items_1 =[
        (producto1,3),
        (producto2,2),
        (producto3,2),
        (producto4,1),
    ]

    items_2 =[
        (producto7,4),
        (producto5,3),
        (producto6,2),
        (producto3,2),
    ]

    items_3 = [
        (producto4,1),
        (producto2,1),
    ]

    items_4 = [
        (producto7,2)
    ]

    # asignamos los items a las distintas ventas
    venta1, venta2, venta3,venta4,venta5,venta6,venta7,venta8,venta9,venta10 = get_ventas_not_items
    print(venta1.fecha)
    print(venta2.fecha)
    print(venta3.fecha)
    print(venta4.fecha)
    print(venta5.fecha)
    print(venta6.fecha)
    print(venta7.fecha)
    print(venta8.fecha)
    print(venta9.fecha)
    print(venta10.fecha)


    ventas.append(create_venta_with_items(venta1, items_3))
    ventas.append(create_venta_with_items(venta2,items_3))
    ventas.append(create_venta_with_items(venta3,items_4))
    ventas.append(create_venta_with_items(venta4, items_3))
    ventas.append(create_venta_with_items(venta5, items_2))
    ventas.append(create_venta_with_items(venta6, items_1))
    ventas.append(create_venta_with_items(venta7, items_3))
    ventas.append(create_venta_with_items(venta8, items_1))
    ventas.append(create_venta_with_items(venta9, items_2))
    ventas.append(create_venta_with_items(venta10, items_4))

    return ventas