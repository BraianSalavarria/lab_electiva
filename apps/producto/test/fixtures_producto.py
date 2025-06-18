from decimal import Decimal

import pytest
from pytest import mark

from .fixtures_categoria import get_categorias, get_categoria
from apps.usuario.test.fixture_user import api_client,get_user,get_user_admin,get_authenticated_client
from ..models import Categoria, Producto



def create_producto(categoria,nombre,precio,stock):
    producto, created = Producto.objects.get_or_create(nombre=nombre,categoria=categoria,defaults={'precio':precio,'stock':stock})
    return producto

@pytest.fixture
def get_producto(get_authenticated_client,get_categoria):
    categoria=get_categoria
    producto = create_producto(categoria,'facturas x12',precio=Decimal(11000.00), stock=4)
    return producto


@pytest.fixture
def get_productos(get_authenticated_client,get_categorias):
    productos=[]
    panificacion,embutidos,art_limpieza,art_higiene=get_categorias

    #productos de panificacion
    productos.append(create_producto(panificacion,'facturas (x12)',Decimal("5700.00"),45))
    productos.append(create_producto(panificacion,'facturas (x6)',Decimal("4200.00"),22))
    productos.append(create_producto(panificacion, 'cremona', Decimal("2200.00"), 23))
    productos.append(create_producto(panificacion, 'chalitas', Decimal("2100.00"), 19))
    productos.append(create_producto(panificacion, 'grisines', Decimal("2100.00"), 14))

    #productos de embutidos
    productos.append(create_producto(embutidos, 'mortadela panadini', Decimal("9800.00"), 13))
    productos.append(create_producto(embutidos, 'mortadela 804', Decimal("8600.00"), 16))
    productos.append(create_producto(embutidos, 'jamon crudo', Decimal("9800.00"), 7))
    productos.append(create_producto(embutidos, 'zalamin picado grueso', Decimal("10650.00"), 16))

    #productos de art_limpieza
    productos.append(create_producto(art_limpieza, 'liquido para piso poett', Decimal("5467.00"), 9))
    productos.append(create_producto(art_limpieza, 'lavandina ayudin 1L', Decimal("6730.00"), 12))
    productos.append(create_producto(art_limpieza, 'pastillas para inodoro', Decimal("4250.00"), 7))
    productos.append(create_producto(art_limpieza, 'antigrasa mr musculo', Decimal("7467.80"), 9))
    #productos de higiene personal
    productos.append(create_producto(art_higiene, 'desodorante rexona', Decimal("4000.00"), 10))
    productos.append(create_producto(art_higiene, 'shampoo plusbelle', Decimal("4357.00"), 5))
    productos.append(create_producto(art_higiene, 'jabon tocador dove', Decimal("5597.00"), 8))
    productos.append(create_producto(art_higiene, 'dentrifico colgate x250', Decimal("6355.00"), 9))

    return productos

