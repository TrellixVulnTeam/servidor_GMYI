# Generated by Django 3.2.8 on 2021-11-17 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0052_auto_20211117_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='informacionpersonal',
            name='puesto',
            field=models.CharField(blank=True, max_length=20, verbose_name='Puesto del usuario dentro de la empresa'),
        ),
    ]
