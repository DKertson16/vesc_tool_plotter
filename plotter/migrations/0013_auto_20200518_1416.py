# Generated by Django 3.0.5 on 2020-05-19 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plotter', '0012_auto_20200518_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvrow',
            name='ms_today',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
