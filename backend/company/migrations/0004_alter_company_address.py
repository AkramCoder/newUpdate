# Generated by Django 3.2 on 2023-08-29 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20230828_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.address'),
        ),
    ]