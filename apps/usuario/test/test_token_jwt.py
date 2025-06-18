import pytest

from .fixture_user import get_user, api_client

@pytest.mark.django_db
def test_token_jwt_valido(get_user,api_client):

    data ={
        'username': get_user.username,
        'password': 'unpassword'
    }

    response = api_client.post('/api/v1/token/', data,format='json')

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_token_jwt_credeciales_invalidas(get_user, api_client):
    """Test que verifica el rechazo con credenciales inválidas"""

    data = {
        'username': get_user.username,
        'password': 'password_incorrecto'
    }

    response = api_client.post('/api/v1/token/', data, format='json')

    assert response.status_code == 401
    # Verificar que no se devuelven tokens
    assert 'access' not in response.data
    assert 'refresh' not in response.data


@pytest.mark.django_db
def test_token_jwt_usuario_inexistente(api_client):
    """Test que verifica el rechazo con usuario inexistente"""

    data = {
        'username': 'augusto',
        'password': 'unpassword'
    }

    response = api_client.post('/api/v1/token/', data, format='json')

    assert response.status_code == 401
    # Verificar que no se devuelven tokens
    assert 'access' not in response.data
    assert 'refresh' not in response.data
