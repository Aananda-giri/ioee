# Generated by Django 3.1.7 on 2021-07-09 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuse_attend', '0008_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='collage',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='faculty',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='section',
            field=models.CharField(default=None, max_length=15, null=True),
        ),
    ]
