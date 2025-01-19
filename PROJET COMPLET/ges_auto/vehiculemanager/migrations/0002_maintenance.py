# Generated by Django 5.1.5 on 2025-01-19 19:59

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculemanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_maintenance', models.DateField(verbose_name='Maintenance Date')),
                ('type', models.CharField(max_length=50, verbose_name='Type of Maintenance')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('cout', models.FloatField(verbose_name='Cost')),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('In Progress', 'In Progress')], max_length=50, verbose_name='Status')),
                ('pieces_changees', models.TextField(blank=True, verbose_name='Replaced Parts')),
                ('date_prochaine_maintenance', models.DateField(blank=True, null=True, verbose_name='Next Maintenance Date')),
                ('date_enregistrement', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Recorded')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Date Modified')),
                ('vehicule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehiculemanager.vehicule', verbose_name='Vehicle')),
            ],
            options={
                'verbose_name': 'Maintenance',
                'verbose_name_plural': 'Maintenances',
                'ordering': ['-date_maintenance'],
            },
        ),
    ]
