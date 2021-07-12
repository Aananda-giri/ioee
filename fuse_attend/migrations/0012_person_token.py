# Generated by Django 3.1.7 on 2021-07-09 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuse_attend', '0011_remove_person_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='token',
            field=models.CharField(blank=True, db_index=True, editable=False, max_length=16, unique=True),
        ),
    ]
