# Generated by Django 5.1.6 on 2025-02-15 23:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculemanager', '0002_alter_carburant_cout_unitaire'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carburant',
            name='commentaire',
        ),
        migrations.RemoveField(
            model_name='carburant',
            name='facture',
        ),
        migrations.RemoveField(
            model_name='carburant',
            name='plein_complet',
        ),
        migrations.RemoveField(
            model_name='maintenance',
            name='facture',
        ),
        migrations.RemoveField(
            model_name='maintenance',
            name='kilometrage_actuel',
        ),
        migrations.RemoveField(
            model_name='maintenance',
            name='technicien',
        ),
        migrations.RemoveField(
            model_name='vehicule',
            name='description',
        ),
        migrations.RemoveField(
            model_name='vehicule',
            name='image',
        ),
        migrations.AddField(
            model_name='vehicule',
            name='image_url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name="URL de l'image"),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='cout_total',
            field=models.FloatField(blank=True, null=True, verbose_name='Coût Total'),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='cout_unitaire',
            field=models.FloatField(blank=True, null=True, verbose_name='Coût Unitaire'),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='date_enregistrement',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date d'Enregistrement"),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='Date de Modification'),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='date_prise',
            field=models.DateField(verbose_name='Date Prise'),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='kilometrage_actuel',
            field=models.PositiveIntegerField(verbose_name='Kilométrage Actuel'),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='quantite',
            field=models.FloatField(verbose_name='Quantité (L)'),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='type_carburant',
            field=models.CharField(max_length=50, verbose_name='Type Carburant'),
        ),
        migrations.AlterField(
            model_name='carburant',
            name='vehicule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehiculemanager.vehicule', verbose_name='Véhicule'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='cout',
            field=models.FloatField(verbose_name='Cost'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='date_enregistrement',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Recorded'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='date_maintenance',
            field=models.DateField(verbose_name='Maintenance Date'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Modified'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='date_prochaine_maintenance',
            field=models.DateField(blank=True, null=True, verbose_name='Next Maintenance Date'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='pieces_changees',
            field=models.TextField(blank=True, verbose_name='Replaced Parts'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('In Progress', 'In Progress')], max_length=50, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='type',
            field=models.CharField(max_length=50, verbose_name='Type of Maintenance'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='vehicule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehiculemanager.vehicule', verbose_name='Vehicle'),
        ),
        migrations.AlterField(
            model_name='vehicule',
            name='annee',
            field=models.PositiveIntegerField(verbose_name='Année'),
        ),
        migrations.AlterField(
            model_name='vehicule',
            name='immatriculation',
            field=models.CharField(max_length=50, unique=True, verbose_name='Immatriculation'),
        ),
        migrations.AlterField(
            model_name='vehicule',
            name='kilometrage',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Kilométrage'),
        ),
        migrations.AlterField(
            model_name='vehicule',
            name='status',
            field=models.CharField(choices=[('Disponible', 'Disponible'), ('Indisponible', 'Indisponible')], default='Disponible', max_length=50, verbose_name='Statut'),
        ),
    ]
