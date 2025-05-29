from django_filters import rest_framework as filters, FilterSet
from apps.producto.models import Categoria, Producto


class CategoriaFilter(FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        model = Categoria
        fields = ['nombre']

class ProductoFilter(FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    precio_hasta = filters.NumberFilter(field_name='precio', lookup_expr='lte')
    precio_desde = filters.NumberFilter(field_name='precio', lookup_expr='gte')

    class Meta:
        model = Producto
        fields = ['nombre','precio']