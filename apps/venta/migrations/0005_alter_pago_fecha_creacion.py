# Generated by Django 5.2 on 2025-05-28 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0004_pago_qr_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True),
        ),
    ]
