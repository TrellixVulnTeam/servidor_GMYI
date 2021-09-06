# Generated by Django 3.2.6 on 2021-08-24 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0007_alter_cliente_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='mantenimiento',
            name='encargadoTrabajo',
            field=models.CharField(choices=[('Tecnico', 'Tecnico'), ('Project Manager', 'Project Manager'), ('Ingeniero', 'Ingeniero'), ('Equipo de tecnicos', 'Equipo de Tecnicos'), ('Electrico', 'Electrico'), ('Trainer', 'Trainer')], default='Tecnico', max_length=30),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de realizacion de la cotizacion'),
        ),
    ]