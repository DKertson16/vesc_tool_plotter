# Generated by Django 3.0.5 on 2020-05-16 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plotter', '0010_auto_20200512_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='date_added',
            field=models.DateField(auto_now=True, verbose_name='date uploaded'),
        ),
    ]
