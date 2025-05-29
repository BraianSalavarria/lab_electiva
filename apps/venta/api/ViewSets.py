from datetime import date
from django.conf import settings
from django.db.models import Sum, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from apps.venta.api.filters import VentaFilter, RendicionDiariaFilter, PagoFilter
from apps.venta.api.serializers import VentaSerializer, RendicionDiariaSerializer, PagoSerializer
from apps.venta.models import Venta, ItemVenta, RendicionDiaria
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from apps.venta.models import Pago
from core.permissions import StrictModelPermissions


class VentaViewSet(ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = VentaFilter
    ordering_fields = ['fecha']
    ordering = ['fecha']
    permission_classes = [StrictModelPermissions]
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

############################## Implementacion de Mercado Pago ########################################

    @action(detail=True, methods=['post'])
    def generar_pago(self, request, uuid=None):
        #Generar QR dinámico para la venta
        venta = self.get_object()

        if hasattr(venta, 'pago'):
            return Response({'detalle': 'Ya se generó un pago para esta venta'}, status=status.HTTP_200_OK)

        if (venta.pago_efectuado is True):
            return Response({'detalle':'No se puede generar una orden de pago de una venta ya abonada'}, status=status.HTTP_200_OK)
        
        access_token = settings.MERCADO_PAGO_ACCESS_TOKEN
        user_id = settings.USER_ID
        external_pos_id = settings.EXTERNAL_POS_ID  # Ajuste importante
        ngrok_url = settings.NGROK_URL

        # URL según la documentación de Mercado Pago
        url = f"https://api.mercadopago.com/instore/orders/qr/seller/collectors/{user_id}/pos/{external_pos_id}/qrs"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Preparamos los items para el QR dinámico
        items_data = []
        for item in venta.items.all():
            items_data.append({
                "sku_number": str(item.producto.id),
                "category": "general",
                "title": item.producto.nombre,
                "description": f"Producto: {item.producto.nombre}",
                "unit_price": float(item.producto.precio),
                "quantity": item.cantidad,
                "unit_measure": "unit",
                "total_amount": float(item.subtotal)
            })

        # Estructura para QR dinámico
        datos = {
            "external_reference": str(venta.uuid),
            "title": f"Venta #{venta.id}",
            "description": f"Pago de venta realizada el {venta.fecha}",
            "notification_url": f"https://{ngrok_url}/webhooks/mercadopago/",
            "total_amount": float(venta.total),
            "items": items_data
        }

        print(f"Enviando datos a MercadoPago: {datos}")

        # Realizar petición para crear la orden QR
        resp = requests.put(url, headers=headers, json=datos)

         ############# prueba por terminal ####################
        print(f"Status code: {resp.status_code}")
        print(f"Response: {resp.text}")

        if resp.status_code not in [200, 201]:
            return Response({
                "error": "No se pudo generar el QR dinámico",
                "detalle": resp.text,
                "status_code": resp.status_code
            }, status=resp.status_code)

        data = resp.json()
        qr_data = data.get("qr_data")

        #### verificamos si mercado pago nos asigno un qr ###
        if not qr_data:
            return Response({
                "error": "No se recibió qr_data en la respuesta",
                "detalles": data
            }, status=status.HTTP_404_NOT_FOUND)

        # Guardar el pago con el qr_data
        fecha_hoy = date.today()
        pago = Pago.objects.create(
            venta=venta,
            mercado_pago_order_id=data.get("in_store_order_id"),
            qr_data=qr_data,
            qr_url= request.build_absolute_uri(f"/api/v1/venta/{venta.uuid}/qr/"),
            fecha_creacion= fecha_hoy,
            estado="pendiente"
        )

        return Response({
            "order_id": data.get("in_store_order_id"),
            "qr_url": request.build_absolute_uri(f"/api/v1/venta/{venta.uuid}/qr/"),
            "mensaje": "QR dinámico generado exitosamente"
        }, status=status.HTTP_201_CREATED)




class RendicionDiariaViewSet(ModelViewSet):
    serializer_class = RendicionDiariaSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = RendicionDiariaFilter
    ordering_fields = ['fecha']
    ordering = ['fecha']
    lookup_field = 'uuid'

    def get_queryset(self):
        #Mostramos solo las rendiciones del usuario actual (para probar el query_Set)
        return RendicionDiaria.objects.filter(usuario=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        #Creamos el cierre de caja automático basado en las ventas del día
        # Validamos usando el serializer
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Calculamo los totales de ventas del día para el usuario actual
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

    # Obtenemos historial de todas las rendiciones del usuario (es como un get)
    @action(detail=False, methods=['get'])
    def historial(self, request):
        rendiciones = self.get_queryset().order_by('-fecha')
        serializer = self.get_serializer(rendiciones, many=True)
        return Response(serializer.data)

class PagosViewSet(ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PagoFilter
    ordering_fields = ['fecha_creacion']
    ordering = ['-fecha_creacion']
    lookup_field = 'uuid'