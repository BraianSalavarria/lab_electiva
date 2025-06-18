import  pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.producto.models import Categoria
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()


"""
    # TIPOS DE PARAMETROS Y EL USO DEL '*'
        Existen parametros "posicional" y "Nombrado", los posicionales deben ir un una posicion especifica en la firma del metodo y
        los parametros nombrados, son aquellos que deben ir explicitos en la firma del metodo como nombre=braian
        ¿Para que sirve el *, en la lista de parametros?: Sirve para indicar que todo lo que este despues del * debe ser un parametro
        nombrado.
        
    # DESEMPAQUETAMIENTO MULTIPLE
        Cuando un metodo devuelve mas de un valor ( tupla ), se pueden expecificar en que vbles almacenar cada uno de los valores de 
        la tupla. como el metodo "get_or_create" que devuelde un usuario en caso de encontrarlo y un valor booleano.
"""


def asignar_permisos_completos(usuario, app_label, modelo):
    """
    Asignamos todos los permisos (add, change, delete, view) para el modelo especificado al usuario.
    Parametros:
    usuario: instancia del usuario
    app_label: nombre de la app
    modelo: nombre del modelo - debe ir en minusculas
    """
    content_type = ContentType.objects.get(app_label=app_label, model=modelo)
    permisos = Permission.objects.filter(content_type=content_type)
    usuario.user_permissions.add(*permisos)

    return usuario

def asignar_permisos_especificos(usuario,permiso,modelo):
    """
    Asignamos permisos especificos para un modelo, mediante su codename.
    ¿Que es el codename?:
     El codename es un identificador único que representa cada permiso
     individual dentro del sistema de autenticación y autorización.

     Permisos aceptados-codename:
     "add_modelo"
     "change_modelo"
     "delete_modelo"
     "view_modelo"
    """
    try:
        codename = '{}_{}'.format(permiso,modelo)
        permiso = Permission.objects.get(codename=codename)
        usuario.user_permissions.add(permiso)

    except Permission.DoesNotExist:
        print(f" El permiso '{codename}' no existe.")
    return usuario


def create_user(username, dni, first_name= 'Jesica', last_name='Salavarria', email=None ,password='unpassword'):

    email = '{}@root.com'.format(username) if email is None else email #format permite agregar valores en los literales de plantilla ( {} )
    user, created = User.objects.get_or_create(username=username, email=email)

    if created:
        user.first_name = first_name
        user.last_name = last_name
        user.dni = dni
        user.is_active = True
        user.is_staff = True
        user.set_password(password) #al usar setpassword se hashea la cpntraseña

        #debemos asignar todos los permisos correspodiente
        asignar_permisos_completos(user, 'producto', 'categoria')
        asignar_permisos_completos(user, 'producto', 'producto')
        #asignamos permisos especificos
        asignar_permisos_especificos(user, 'add', 'venta')
        asignar_permisos_especificos(user, 'view', 'venta')
        user.save()
    return user


def create_user_admin(username, dni, first_name= 'Braian', last_name='Salavarria', email=None ,password='unpassword'):

    email = '{}@root.com'.format(username) if email is None else email #format permite agregar valores en los literales de plantilla ( {} )
    user, created = User.objects.get_or_create(username=username, email=email)

    if created:
        user.first_name = first_name
        user.last_name = last_name
        user.dni = dni
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password) #al usar setpassword se hashea la cpntraseña
        #debemos asignar todos los permisos
        asignar_permisos_completos(user, 'producto', 'categoria')
        asignar_permisos_completos(user, 'producto', 'producto')
        asignar_permisos_completos(user,'venta','venta')
        user.save()
    return user

####################################  FIXTURES  ###################################

@pytest.fixture
def get_user():
    test_user=create_user(username='test_user',dni='38997665',first_name='Carlos', last_name='Salavarria', email='test@user.com')
    return test_user


@pytest.fixture
def get_user_admin():
    test_user_admin=create_user_admin(username='test_user_admin',dni='38998776',first_name='Braian', last_name='Salavarria', email='test@admin.com')
    return test_user_admin


@pytest.fixture
def get_authenticated_client(get_user, api_client):

    # Crear token JWT para el usuario
    refresh = RefreshToken.for_user(get_user)
    access_token = str(refresh.access_token)

    # Configurar las credenciales en el cliente
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client #devuelve un apicliente con un usuario ya autentificado


@pytest.fixture
def get_authenticated_client_admin(get_user_admin, api_client):
    # Crear token JWT para el usuario
    refresh = RefreshToken.for_user(get_user_admin)
    access_token = str(refresh.access_token)

    # Configurar las credenciales en el cliente
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client #devuelve un apicliente con un usuario ya autentificado
