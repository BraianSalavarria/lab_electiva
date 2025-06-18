import pytest
from apps.producto.models import Categoria


@pytest.fixture
def get_categoria():
    categoria1, _ = Categoria.objects.get_or_create(
        nombre='panificacion'
    )
    return categoria1

@pytest.fixture
def get_categorias():
    categoria1, _ = Categoria.objects.get_or_create(
        nombre='panificacion'
    )
    categoria2, _ = Categoria.objects.get_or_create(
        nombre='embutidos'
    )
    categoria3, _ = Categoria.objects.get_or_create(
        nombre='art.Limpieza'
    )
    categoria4, _ = Categoria.objects.get_or_create(
        nombre='art.Higiene'
    )
    return categoria1, categoria2, categoria3, categoria4