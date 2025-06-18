import pytest
from .fixtures_categoria import get_categorias, get_categoria
from apps.usuario.test.fixture_user import api_client,get_user,get_user_admin,get_authenticated_client
from ..models import Categoria


#test para obtener una lista de categorias, ordenamas alfabeticamente con usuario autentificado
@pytest.mark.django_db
def test_get_categorias_authenticated_client(get_authenticated_client, get_categorias):
    cliente=get_authenticated_client
    response = cliente.get('/api/v1/categoria/')

    # debemos acceder al atributo results de data, ya que usamos paginacion
    categorias = response.data['results']
    assert response.status_code == 200
    assert len(response.data) == 4
    assert categorias[0]['nombre'] == 'art.Higiene'
    assert categorias[1]['nombre'] == 'art.Limpieza'
    assert categorias[2]['nombre'] == 'embutidos'
    assert categorias[3]['nombre'] == 'panificacion'

#test para usuario no autentificado
@pytest.mark.django_db
def test_get_categorias_not_authenticated_client(api_client, get_categorias):
    cliente=api_client
    response = cliente.get('/api/v1/categoria/')

    assert response.status_code == 401
    assert str(response.data['detail']) == 'Las credenciales de autenticación no se proveyeron.'
    assert response.status_text == 'Unauthorized'

#test para agregar(listo), eliminar y modificar una categoria

#test para la creacion de una categoria con cliente autenticado
@pytest.mark.django_db
def test_post_categoria(get_authenticated_client):
    cliente = get_authenticated_client
    data ={
        "nombre":"perfumeria"
    }
    response = cliente.post('/api/v1/categoria/',data=data,format='json')
    assert response.status_code == 201
    assert Categoria.objects.filter(nombre='perfumeria').exists() == True


#testeamos la creacion de una categoria ya existente
@pytest.mark.django_db
def test_post_categoria_existente(get_authenticated_client,get_categoria):
    cliente = get_authenticated_client
    data ={
        "nombre":"panificacion"
    }
    response = cliente.post('/api/v1/categoria/',data=data,format='json')
    assert response.status_code == 400                                       #podria ser el error 409? de conflicto con el recurso?
    assert Categoria.objects.filter(nombre='panificacion').exists() == True
    assert str(response.data['nombre'][0]) == 'Ya existe un/a categoria con este/a nombre.'


#testeamos la modificacion de una categoria
@pytest.mark.django_db
def test_patch_categoria(get_authenticated_client,get_categoria):
    cliente = get_authenticated_client
    categoria = get_categoria
    data ={
        "nombre":"panificacion mod"
    }
    response = cliente.patch('/api/v1/categoria/{}/'.format(categoria.uuid),data=data,format='json')
    assert response.status_code == 200
    assert Categoria.objects.filter(nombre='panificacion mod').exists() == True

#testeamos que al modificar una categoria esta no pueda tener el nombre de otra categoria
@pytest.mark.django_db
def test_path_categoria_nombre_usado(get_authenticated_client,get_categorias):
    cliente = get_authenticated_client
    categoria_mod,c1,_,_ = get_categorias
    data ={
        "nombre":"embutidos"
    }
    response= cliente.patch('/api/v1/categoria/{}/'.format(categoria_mod.uuid),data=data,format='json')
    assert response.status_code == 400
    assert str(response.data['nombre'][0]) == 'Ya existe un/a categoria con este/a nombre.'

#testeamos la eliminacion de una categoria
@pytest.mark.django_db
def test_delete_categoria(get_authenticated_client,get_categoria):
    cliente = get_authenticated_client
    categoria = get_categoria
    response = cliente.delete('/api/v1/categoria/{}/'.format(categoria.uuid))
    assert response.status_code == 204
    assert Categoria.objects.filter(nombre=categoria.nombre).exists() == False

#testeamos la elimicion de una categoria para un usuario no autentificado
@pytest.mark.django_db
def test_delete_categoria_not_authenticated_client(api_client,get_categoria):
    cliente = api_client
    categoria = get_categoria
    response = cliente.delete('/api/v1/categoria/{}/'.format(categoria.uuid))
    assert response.status_code == 401
    assert str(response.data['detail']) == 'Las credenciales de autenticación no se proveyeron.'
    assert response.status_text == 'Unauthorized'

