import pytest
from apps.usuario.test.fixture_user import get_authenticated_client,api_client,get_user,get_authenticated_client_admin, get_user_admin
from apps.producto.test.fixtures_categoria import get_categorias,get_categoria
from apps.producto.test.fixtures_producto import get_productos,get_producto
from .fixtures_venta import get_venta,get_ventas,get_ventas_not_items,get_item_venta,get_venta_not_item
from ... import venta
from ...producto.models import Producto


#testeamos que se crean y listan las 10 ventas realizadas en diferentes fechas
@pytest.mark.django_db
def test_get_ventas(get_authenticated_client,get_ventas):
    cliente = get_authenticated_client
    response = cliente.get('/api/v1/venta/')
    assert response.status_code == 200
    assert len(response.data['results']) == 10

#testeamos que al realizar la venta, el stock del producto se reduzca, se agrega una venta y se reduce el stock
@pytest.mark.django_db
def test_stock_producto_venta(get_authenticated_client,get_producto):
    cliente = get_authenticated_client
    producto = get_producto
    data = {
        "items": [
            {
                "id":producto.id,
                "cantidad":3
            }
        ]
    }

    response = cliente.post('/api/v1/venta/',data,format='json')
    assert response.status_code == 201
    assert  Producto.objects.get(id=producto.id).stock == 1

@pytest.mark.django_db
def test_stock_insuficiente(get_authenticated_client,get_producto):
    cliente = get_authenticated_client
    producto = get_producto
    data = {
        "items": [
            {
                "id": producto.id,
                "cantidad": 9
            }
        ]
    }

    response = cliente.post('/api/v1/venta/', data, format='json')
    assert response.status_code == 400
    assert str(response.data['items'][0]) == 'Stock insuficiente para el producto facturas x12'


#testeamos el total de una venta
@pytest.mark.django_db
def test_total_venta(get_authenticated_client,get_producto):
    cliente = get_authenticated_client
    producto = get_producto
    print(producto.nombre, producto.precio)
    data = {
        "items": [
            {
                "id": producto.id,
                "cantidad": 2
            }
        ]
    }

    response = cliente.post('/api/v1/venta/', data, format='json')
    assert response.status_code == 201
    assert  response.data['total'] == '22000.00'






#testeamos cuando se agregar un id de producto incorrecto
@pytest.mark.django_db
def test_id_incorrecto_venta(get_authenticated_client):
    cliente = get_authenticated_client
    data = {
        "items": [
            {
                "id": 34,
                "cantidad": 9
            }
        ]
    }

    response = cliente.post('/api/v1/venta/', data, format='json')
    assert response.status_code == 400
    assert str(response.data['items'][0]) == 'El producto con id 34 no existe'


#testeamos el error al no agregar items en una venta
@pytest.mark.django_db
def test_id_incorrecto_venta(get_authenticated_client):
    cliente = get_authenticated_client
    data = {
        "items": [
            {

            }
        ]
    }

    response = cliente.post('/api/v1/venta/', data, format='json')
    assert response.status_code == 400
    assert str(response.data['items'][0]) == 'Cada item debe tener un id de producto y una cantidad'


#testeamos el error cuando no se le proporciona items a una venta
@pytest.mark.django_db
def test_id_incorrecto_venta(get_authenticated_client):
    cliente = get_authenticated_client
    data = {

    }

    response = cliente.post('/api/v1/venta/', data, format='json')
    assert response.status_code == 400
    assert str(response.data['items'][0]) == 'Debe proporcionar al menos un item para la venta'


#testeamos el filtro de las fechas
@pytest.mark.django_db
def test_rango_fechas_ventas(get_authenticated_client,get_ventas):
    cliente = get_authenticated_client
    response = cliente.get('/api/v1/venta/?fecha_desde={}&fecha_hasta={}'.format('2025-07-15','2025-07-17'))
    assert response.status_code == 200
    assert len(response.data['results']) == 6


#testeamos el filtro de las ventas desde un monto específico
@pytest.mark.django_db
def test_filtro_monto_total_ventas(get_authenticated_client,get_ventas):
    cliente = get_authenticated_client
    response = cliente.get('/api/v1/venta/?total_desde={}'.format('30000'))
    assert response.status_code == 200
    assert len(response.data['results']) == 4


#testeamos el filtro de las ventas desde un rando del monto total
@pytest.mark.django_db
def test_filtro_monto_total_ventas(get_authenticated_client,get_ventas):
    cliente = get_authenticated_client
    response = cliente.get('/api/v1/venta/?total_desde={}&total_hasta={}'.format('20000','70000'))
    assert response.status_code == 200
    assert len(response.data['results']) == 4


#testeamos el permiso denegado a un usuario para eliminar una venta
@pytest.mark.django_db
def test_delete_venta_not_user_authorized(get_authenticated_client,get_venta):
    cliente = get_authenticated_client
    venta = get_venta
    response = cliente.delete('/api/v1/venta/{}/'.format(venta.uuid))
    assert response.status_code == 403
    assert str(response.data['detail']) == 'Usted no tiene permiso para realizar esta acción.'

