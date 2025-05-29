import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import qrcode
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.venta.models import Venta
import requests
from django.conf import settings

#Vista para mostrar el QR de pago dinámico
def mostrar_qr_pago(request, venta_uuid):
    venta = get_object_or_404(Venta, uuid=venta_uuid)

    if not hasattr(venta, 'pago'):
        return render(request, 'error.html', {
            'mensaje': 'No hay pago generado para esta venta'
        })

    # Generamos el QR con el qr_data
    if venta.pago.qr_data:
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            # Para QR dinámico, el qr_data ya viene listo para usar
            qr.add_data(venta.pago.qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()

            return render(request, 'qr_pago.html', {
                'qr_base64': qr_base64,
                'venta': venta,
                'qr_data': venta.pago.qr_data,
                'es_qr_dinamico': True
            })

        except Exception as e:
            return render(request, 'error.html', {
                'mensaje': f'Error al generar el QR: {str(e)}'
            })

    return render(request, 'error.html', {
        'mensaje': 'No se pudo generar el código QR'
    })

#Webhook permite recibir notificaciones de MercadoPago QR Dinámico para consultar el estado de un pago

@csrf_exempt
@require_POST
def webhook_mercadopago(request):

    try:
        data = json.loads(request.body)
        print(f"Webhook QR dinámico recibido: {data}")


        topic = data.get('topic')
        resource = data.get('resource')

        # Si es una notificación de merchant_order (común en QR dinámico)
        if topic == 'merchant_order' and resource:
            # Obtener información de la orden
            url = f"https://api.mercadopago.com/merchant_orders/{resource.split('/')[-1]}"
            headers = {
                "Authorization": f"Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                order_info = response.json()
                external_reference = order_info.get('external_reference')

                print(f"Merchant Order: {resource}, External Reference: {external_reference}")

                # Procesar los pagos de la orden
                payments = order_info.get('payments', [])

                if external_reference and payments:
                    try:
                        venta = Venta.objects.get(uuid=external_reference)

                        # Verificar el estado del pago más reciente
                        for payment in payments:
                            status = payment.get('status')
                            payment_id = payment.get('id')

                            if hasattr(venta, 'pago'):
                                if status == 'approved':
                                    venta.pago.estado = 'aprobado'
                                    venta.pago_efectuado = True
                                    print(f"✅ Pago QR dinámico aprobado para venta {venta.uuid}")

                                elif status == 'rejected':
                                    venta.pago.estado = 'rechazado'
                                    venta.pago_efectuado = False
                                    print(f"❌ Pago QR dinámico rechazado para venta {venta.uuid}")

                                elif status in ['pending', 'in_process']:
                                    venta.pago.estado = 'pendiente'
                                    venta.pago_efectuado = False
                                    print(f"⏳ Pago QR dinámico pendiente para venta {venta.uuid}")

                                # Actualizar payment_id si no existe
                                if not venta.pago.mercado_pago_payment_id and payment_id:
                                    venta.pago.mercado_pago_payment_id = str(payment_id)

                                venta.pago.save()
                                venta.save()

                    except Venta.DoesNotExist:
                        print(f"❌ Venta no encontrada: {external_reference}")

        # También manejar notificaciones directas de payment
        elif topic == 'payment' and resource:
            payment_id = resource.split('/')[-1]

            url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
            headers = {
                "Authorization": f"Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                payment_info = response.json()
                external_reference = payment_info.get('external_reference')
                status = payment_info.get('status')

                print(f"Payment ID: {payment_id}, Status: {status}, External Reference: {external_reference}")

                if external_reference:
                    try:
                        venta = Venta.objects.get(uuid=external_reference)

                        if hasattr(venta, 'pago'):
                            if status == 'approved':
                                venta.pago.estado = 'aprobado'
                                venta.pago_efectuado = True

                            elif status == 'rejected':
                                venta.pago.estado = 'rechazado'
                                venta.pago_efectuado = False

                            elif status in ['pending', 'in_process']:
                                venta.pago.estado = 'pendiente'
                                venta.pago_efectuado = False

                            if not venta.pago.mercado_pago_payment_id:
                                venta.pago.mercado_pago_payment_id = payment_id

                            venta.pago.save()
                            venta.save()

                    except Venta.DoesNotExist:
                        print(f"❌ Venta no encontrada: {external_reference}")

        return JsonResponse({'status': 'ok'})

    except Exception as e:
        print(f"Error en webhook QR dinámico: {str(e)}")
        return JsonResponse({'status': 'error'}, status=400)