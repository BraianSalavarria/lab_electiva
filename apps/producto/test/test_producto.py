import pytest
from .fixtures_categoria import get_categorias, get_categoria
from apps.usuario.test.fixture_user import api_client,get_user,get_user_admin,get_authenticated_client
from .fixtures_producto import get_producto, get_productos
from ..models import Producto
from ... import producto


#testemos una lista de productos -cantidad y orden alfabetico
@pytest.mark.django_db
def test_get_productos(get_authenticated_client, get_productos):
    cliente = get_authenticated_client
    response = cliente.get('/api/v1/producto/')
    productos = response.data['results']
    assert response.status_code == 200
    assert len(response.data['results']) == 17
    assert productos[0]['nombre'] == 'antigrasa mr musculo'
    assert productos[1]['nombre'] == 'chalitas'
    assert productos[2]['nombre'] == 'cremona'
    assert productos[3]['nombre'] == 'dentrifico colgate x250'

#testeamos que no se pueda guardar un producto que no tenga stock
@pytest.mark.django_db
def test_producto_sin_stock(get_authenticated_client, get_categoria):
    cliente = get_authenticated_client
    categoria = get_categoria
    data ={
        "nombre": "Pan dulce",
        "precio": 2500.00,
        "stock": 0,
        "categoria": categoria.uuid
    }
    response = cliente.post('/api/v1/producto/', data, format='json')
    assert response.status_code == 400
    assert str(response.data['stock'][0]) == 'No ha proporcionado stock del producto'

#testeamos que no se pueda almacenar un producto que no tenga un precio establecido
@pytest.mark.django_db
def test_producto_sin_precio(get_authenticated_client, get_categoria):
    cliente = get_authenticated_client
    categoria = get_categoria
    data ={
        "nombre": "Pan dulce",
        "precio": 0,
        "stock": 10,
        "categoria": categoria.uuid
    }
    response = cliente.post('/api/v1/producto/', data, format='json')
    assert response.status_code == 400
    assert response.data['precio'][0] == 'precio de producto invalido'

#testeamos el filtro de precios en productos
@pytest.mark.django_db
def test_filtro_precios_producto(get_authenticated_client, get_productos):
    cliente = get_authenticated_client
    categoria = get_categoria
    response = cliente.get('/api/v1/producto/?precio_hasta=4000')
    assert response.status_code == 200
    assert len(response.data['results']) == 4

#testemos la accion personalizada para un producto con stock bajo
@pytest.mark.django_db
def test_check_stock(get_authenticated_client, get_producto):
    cliente = get_authenticated_client
    producto = get_producto
    response = cliente.get('/api/v1/producto/{}/check_stock/'.format(producto.uuid))
    assert response.status_code == 200
    assert response.data['stock'] == 'Stock de facturas x12 bajo: 4'

#testeamos la eliminacion de un producto
@pytest.mark.django_db
def test_delete_producto(get_authenticated_client, get_productos):
    cliente = get_authenticated_client
    producto, *_ = get_productos
    print(producto.nombre, producto.categoria.nombre)
    response = cliente.delete('/api/v1/producto/{}/'.format(producto.uuid))
    assert response.status_code == 204
    assert Producto.objects.filter(nombre=producto.nombre, categoria=producto.categoria).exists() == False

@pytest.mark.django_db
def test_patch_producto(get_authenticated_client, get_producto):
    producto=get_producto
    print(producto.nombre)
    data ={
        "nombre": "facturas x24",
    }
    cliente = get_authenticated_client
    response = cliente.patch('/api/v1/producto/{}/'.format(producto.uuid), data, format='json')
    assert response.status_code == 200
    assert Producto.objects.filter(nombre="facturas x24", categoria=producto.categoria).exists() == True


@pytest.mark.django_db
def test_post_producto(get_authenticated_client, get_categoria):
    cliente = get_authenticated_client
    categoria = get_categoria
    data = {
        "nombre": "trapo para piso",
        "precio": 1100.00,
        "stock": 33,
        "categoria": categoria.uuid
    }
    response = cliente.post('/api/v1/producto/', data, format='json')
    assert response.status_code == 201
    assert Producto.objects.filter(nombre="trapo para piso", categoria=categoria).exists() == True