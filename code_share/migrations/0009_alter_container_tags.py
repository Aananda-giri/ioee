# Generated by Django 4.1.5 on 2023-07-08 15:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_share', '0008_alter_container_unique_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), default=list, null=True, size=None),
        ),
    ]
