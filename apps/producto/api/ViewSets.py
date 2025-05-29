from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.producto.api.filters import CategoriaFilter, ProductoFilter
from apps.producto.api.serializers import CategoriaSerializer, ProductoSerializer
from apps.producto.models import Categoria, Producto
from core.permissions import StrictModelPermissions


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre']
    ordering = ['nombre']
    permission_classes = [StrictModelPermissions]
    lookup_field = 'uuid'

    @action(detail=True, methods=["get"])
    def productos(self, request, uuid=None):
        categoria = self.get_object()
        productos = categoria.productos.all()
        return Response(ProductoSerializer(productos, many=True).data)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ProductoFilter
    ordering_fields = ['nombre']
    ordering = ['nombre']
    permission_classes = [StrictModelPermissions]
    lookup_field = 'uuid'

    @action(detail=True, methods=['get'])
    def check_stock(self, request, uuid=None):
        producto = self.get_object()
        if producto.stock == 0:
            return Response({'stock': 'Sin stock disponible'}, status=status.HTTP_200_OK)
        elif producto.stock >= 5:
            return Response({'stock': f'Stock de {producto.nombre} disponible: {producto.stock}'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'stock': f'Stock de {producto.nombre} bajo: {producto.stock}'}, status=status.HTTP_200_OK)
