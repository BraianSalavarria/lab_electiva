from django_filters.rest_framework import FilterSet, filters
from apps.venta.models import Venta, RendicionDiaria, Pago


class VentaFilter(FilterSet):
    total = filters.NumberFilter(field_name='total', lookup_expr='iexact')
    total_desde = filters.NumberFilter(field_name='total', lookup_expr='gte')
    total_hasta = filters.NumberFilter(field_name='total', lookup_expr='lte')
    fecha = filters.DateFilter(field_name='fecha', lookup_expr='iexact')
    fecha_desde = filters.DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = filters.DateFilter(field_name='fecha', lookup_expr='lte')
    usuario_nombre = filters.CharFilter(field_name='usuario__username', lookup_expr='exact')
    pago_efectuado = filters.BooleanFilter(field_name='pago_efectuado')

    class Meta:
        model = Venta
        fields = ['fecha','total','usuario','pago_efectuado']

class RendicionDiariaFilter(FilterSet):
    nombre=filters.CharFilter(field_name='usuario__username', lookup_expr='exact')
    fecha = filters.DateFilter(field_name='fecha', lookup_expr='exact')

    class Meta:
        model = RendicionDiaria
        fields = ['fecha','usuario']

class PagoFilter(FilterSet):
    fecha=filters.DateFilter(field_name='fecha_creacion')
    estado=filters.CharFilter(field_name='estado', lookup_expr='iexact')
    venta=filters.CharFilter(field_name='venta__uuid', lookup_expr='iexact')
    order_id = filters.CharFilter(field_name='mercado_pago_order_id', lookup_expr='exact')

    class Meta:
        model = Pago
        fields = ['estado','fecha_creacion','venta','mercado_pago_order_id']