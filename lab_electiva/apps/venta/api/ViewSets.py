from datetime import date
from django.db.models import Sum, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from rest_framework.viewsets import ModelViewSet

from apps.venta.api.filters import VentaFilter
from apps.venta.api.serializers import VentaSerializer, RendicionDiariaSerializer
from apps.venta.models import Venta, ItemVenta, RendicionDiaria


class VentaViewSet(ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VentaFilter
    lookup_field = 'uuid'

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Crear el serializer para validar
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Obtener los productos validados del contexto del serializer
        productos_validados = serializer.context.get('productos_validados', [])

        # Crear la venta
        venta = Venta.objects.create(
            usuario=request.user,
            total=0
        )
        total_venta = 0

        # Procesar cada item
        for item_validado in productos_validados:
            producto = item_validado['producto']
            cantidad = item_validado['cantidad']

            # Crear el item de venta
            item_venta = ItemVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad
            )

            # Actualizar el stock del producto
            producto.stock -= cantidad
            producto.save()

            # Acumular el subtotal
            subtotal = producto.precio * cantidad
            total_venta += subtotal

        # Actualizar el total de la venta
        venta.total = total_venta
        venta.save()

        # Devolver la respuesta con los datos de la venta creada
        response_serializer = self.get_serializer(venta)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class RendicionDiariaViewSet(ModelViewSet):
    serializer_class = RendicionDiariaSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        """Mostrar solo las rendiciones del usuario actual"""
        return RendicionDiaria.objects.filter(usuario=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear cierre de caja automático basado en las ventas del día"""
        # Validar usando el serializer
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Calcular totales de ventas del día para el usuario actual
        fecha_hoy = date.today()
        ventas_del_dia = Venta.objects.filter(
            usuario=request.user,
            fecha=fecha_hoy
        ).aggregate(
            total_monto=Sum('total'),
            total_ventas=Count('id')
        )

        # Crear la rendición diaria
        rendicion = RendicionDiaria.objects.create(
            usuario=request.user,
            monto_total=ventas_del_dia['total_monto'] or 0,
            cantidad_ventas=ventas_del_dia['total_ventas'] or 0
        )

        # Serializar la respuesta
        response_serializer = self.get_serializer(rendicion)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def historial(self, request):
        """Obtener historial de todas las rendiciones del usuario"""
        rendiciones = self.get_queryset().order_by('-fecha')
        serializer = self.get_serializer(rendiciones, many=True)
        return Response(serializer.data)