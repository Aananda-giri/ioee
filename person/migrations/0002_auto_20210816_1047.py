# Generated by Django 3.2.6 on 2021-08-16 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='fathers_name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='mothers_name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
