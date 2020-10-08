# Generated by Django 3.0.5 on 2020-05-12 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plotter', '0004_auto_20200511_2153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propeller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='propeller title')),
                ('description', models.CharField(max_length=200, null=True, verbose_name='propeller description')),
            ],
            options={
                'db_table': 'propellers',
            },
        ),
        migrations.RemoveField(
            model_name='build',
            name='propellor',
        ),
        migrations.AlterField(
            model_name='build',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='build', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='build',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='build', to='plotter.Board'),
        ),
        migrations.AlterField(
            model_name='build',
            name='controller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='build', to='plotter.Controller'),
        ),
        migrations.AlterField(
            model_name='build',
            name='foil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='build', to='plotter.Foil'),
        ),
        migrations.AlterField(
            model_name='build',
            name='motor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='build', to='plotter.Motor'),
        ),
        migrations.DeleteModel(
            name='Propellor',
        ),
        migrations.AddField(
            model_name='build',
            name='propeller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='build', to='plotter.Propeller'),
        ),
    ]