# Generated by Django 5.2 on 2025-05-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='pago_efectuado',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
