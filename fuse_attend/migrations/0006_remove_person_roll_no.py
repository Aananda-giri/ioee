# Generated by Django 3.1.7 on 2021-07-09 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fuse_attend', '0005_auto_20210709_0417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='roll_no',
        ),
    ]
