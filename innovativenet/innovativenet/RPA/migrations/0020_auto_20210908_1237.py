# Generated by Django 3.2.6 on 2021-09-08 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0019_auto_20210906_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 8, 0, 0), null=True, verbose_name='Fecha de realizacion de la cotizacion'),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='Titulo',
            field=models.CharField(blank=True, choices=[('Revision y limpieza de panel de alarmas / Remoto', 'Revision y limpieza de panel de alarmas / Remoto'), ('Revision y limpieza de sensores de humo', 'Revision y limpieza de sensores de humo'), (' Revision y limpieza de estrobos -cornetas - campanas-mixtos', 'Revision y limpieza de estrobos -cornetas - campanas-mixtos'), ('Revision y limpieza de Fuentes de poder', 'Revision y limpieza de Fuentes de poder'), ('Revision y limpieza Palancas  de activacion', 'Revision y limpieza Palancas  de activacion'), ('Revision y limpieza Modulos monitores de Flujo', 'Revision y limpieza Modulos monitores de Flujo'), ('Revision y limpieza sensores de ductos de aire', 'Revision y limpieza sensores de ductos de aire'), ('Revision y limpieza Sensor de humo tipo Beam', 'Revision y limpieza Sensor de humo tipo Beam'), ('Revision y limpieza de modulos de Control', 'Revision y limpieza de modulos de Control'), ('Revision y limpieza de modulo de control CT1 o CT2', 'Revision y limpieza de modulo de control CT1 o CT2'), ('Revision y limpieza de modulo releevador CR', 'Revision y limpieza de modulo releevador CR'), ('Revision y Verificacion de resistencias de fin de linea', 'Revision y Verificacion de resistencias de fin de linea'), ('Cambiar ubicaciones Herramientas y personal (mover el punto A al punto B)', 'Cambiar ubicaciones Herramientas y personal (mover el punto A al punto B)'), ('Relleno de informe', 'Relleno de informe'), ('Prueba de comunicación de datos entre panel y dispositivos, asi como los loops.', 'Prueba de comunicación de datos entre panel y dispositivos, asi como los loops.')], max_length=200),
        ),
    ]
