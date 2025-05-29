from rest_framework import serializers
from apps.venta.models import Venta, ItemVenta, Producto, RendicionDiaria, Pago
from datetime import date


class ItemVentaSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ItemVenta
        fields = [
            'producto',
            'cantidad',
            'subtotal',
        ]


class ItemVentaReadSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_precio = serializers.DecimalField(source='producto.precio', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ItemVenta
        fields = [
            'producto',
            'producto_nombre',
            'producto_precio',
            'cantidad',
            'subtotal',
        ]


class VentaSerializer(serializers.ModelSerializer):
    items = ItemVentaReadSerializer(many=True, read_only=True)

    # Campos específicos del usuario
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Venta
        fields = [
            'uuid',
            'id',
            'usuario_id',
            'usuario_nombre',
            'fecha',
            'pago_efectuado',
            'items',
            'total',
        ]
        read_only_fields = ['uuid', 'fecha', 'total', 'usuario_id', 'usuario_nombre']

    def validate(self, data):
        #Validamo los items proporcionados en el request
        request = self.context.get('request')
        if not request:
            return data

        # Validamos que se proporcionen los items
        if 'items' not in request.data:
            raise serializers.ValidationError(
                {'items': 'Debe proporcionar al menos un item para la venta'}
            )

        items_data = request.data.get('items')
        if not isinstance(items_data, list):
            items_data = [items_data]

        if not items_data:
            raise serializers.ValidationError(
                {'items': 'No hay items que vender'}
            )

        # Validar todos los productos y stock antes de crear la venta
        productos_validados = []

        for item_data in items_data:
            producto_id = item_data.get('id')
            cantidad = item_data.get('cantidad')

            # Validar datos del item
            if not producto_id or not cantidad:
                raise serializers.ValidationError(
                    {'items': 'Cada item debe tener un id de producto y una cantidad'}
                )

            try:
                # Obtener el producto
                producto = Producto.objects.get(id=producto_id)

                # Validar stock disponible
                if producto.stock < cantidad:
                    raise serializers.ValidationError(
                        {'items': f'Stock insuficiente para el producto {producto.nombre}'}
                    )

                # Guardar producto y cantidad para usar después
                productos_validados.append({
                    'producto': producto,
                    'cantidad': cantidad
                })

            except Producto.DoesNotExist:
                raise serializers.ValidationError(
                    {'items': f"El producto con id {producto_id} no existe"}
                )

        # Guardar los productos validados en el contexto para que el ViewSet los use
        self.context['productos_validados'] = productos_validados
        return data



class RendicionDiariaSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = RendicionDiaria
        fields = [
            'uuid',
            'fecha',
            'monto_total',
            'cantidad_ventas',
            'usuario',
            'usuario_nombre'
        ]
        read_only_fields = ['uuid', 'fecha', 'monto_total', 'cantidad_ventas', 'usuario', 'usuario_nombre']

    def validate(self, data):
        #Validamos que no exista ya una rendición para el usuario en la fecha actual
        request = self.context.get('request')
        if not request:
            return data

        # Verificar si ya existe una rendición para hoy
        fecha_hoy = date.today()
        if RendicionDiaria.objects.filter(usuario=request.user, fecha=fecha_hoy).exists():
            raise serializers.ValidationError(
                'Ya existe una rendición para el día de hoy'
            )

        return data

class PagoSerializer(serializers.ModelSerializer):
    venta = serializers.PrimaryKeyRelatedField(queryset=Venta.objects.all())
    class Meta:
        model= Pago
        fields = [
            'uuid',
            'venta',
            'estado',
            'fecha_creacion',
            'mercado_pago_order_id',
            'mercado_pago_payment_id',
            'qr_url',
        ]