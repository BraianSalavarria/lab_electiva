from rest_framework import serializers

from apps.producto.models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categoria
        fields=[
            'uuid',
            'id',
            'nombre',
        ]


class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(queryset=Categoria.objects.all(),slug_field='uuid')
    class Meta:
        model=Producto
        fields = [
            'uuid',
            'id',
            'nombre',
            'precio',
            'categoria',
            'stock'
        ]

    def validate_stock(self, data):
        if data <= 0:
            raise serializers.ValidationError(f'No ha proporcionado stock del producto')
        return data

    def validate_precio(self, data):
        if data <= 0:
            raise serializers.ValidationError(f'precio de producto invalido')
        return data