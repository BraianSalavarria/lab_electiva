from django_filters.rest_framework import FilterSet, filters

from apps.venta.models import Venta, RendicionDiaria


class VentaFilter(FilterSet):
    total = filters.NumberFilter(field_name='total', lookup_expr='iexact')
    total_desde = filters.NumberFilter(field_name='total', lookup_expr='gte')
    total_hasta = filters.NumberFilter(field_name='total', lookup_expr='lte')
    fecha = filters.DateFilter(field_name='fecha', lookup_expr='iexact')
    fecha_desde = filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = filters.DateFilter(field_name='fecha', lookup_expr='lte')
    usuario_nombre = filters.CharFilter(field_name='usuario__username', lookup_expr='iexact')

    class Meta:
        model = Venta
        fields = ['fecha','total','usuario']

class RendicionDiariaFilter(FilterSet):

    class Meta:
        model = RendicionDiaria
        fields = ['fecha','usuario']