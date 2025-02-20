# Generated by Django 5.1.6 on 2025-02-16 19:13

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trajetmanager', '0001_initial'),
        ('vehiculemanager', '0004_remove_vehicule_image_url_vehicule_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='trajet',
            name='cout_estime',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='date_creation',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='depart_lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude départ'),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='depart_lon',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude départ'),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='destination_lat',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude destination'),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='destination_lon',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude destination'),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='distance',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Distance (km)'),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='personnel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Personnel'),
        ),
        migrations.AlterField(
            model_name='trajet',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehiculemanager.vehicule', verbose_name='Véhicule'),
        ),
    ]
