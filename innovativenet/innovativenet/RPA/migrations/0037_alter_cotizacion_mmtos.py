# Generated by Django 3.2.8 on 2021-11-03 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0036_auto_20211103_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='mmtos',
            field=models.ManyToManyField(blank=True, null=True, related_name='mantenimientosCotizacion', to='RPA.Mantenimiento'),
        ),
    ]