# Generated by Django 3.2.8 on 2021-11-09 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0044_auto_20211109_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='nombre_servicio',
            name='dispositivo',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Dispositivo al que se le aplica el mantenimiento'),
        ),
    ]