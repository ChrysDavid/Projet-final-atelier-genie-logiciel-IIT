# Generated by Django 5.1.6 on 2025-02-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculemanager', '0003_remove_carburant_commentaire_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicule',
            name='image_url',
        ),
        migrations.AddField(
            model_name='vehicule',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vehicules/', verbose_name='Image du véhicule'),
        ),
    ]
