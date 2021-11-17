# Generated by Django 3.2.8 on 2021-11-17 19:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RPA', '0046_auto_20211111_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sufijo', models.CharField(blank=True, max_length=3, verbose_name='Ej. Lic., Ing.')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='mantenimiento',
            options={'ordering': ['encargadoTrabajo1', 'cantidaddedispositivos']},
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 17, 0, 0), null=True, verbose_name='Fecha de realizacion de la cotizacion'),
        ),
        migrations.DeleteModel(
            name='Dispositivo',
        ),
    ]
