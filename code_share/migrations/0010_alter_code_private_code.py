# Generated by Django 3.2.6 on 2021-12-28 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_share', '0009_auto_20211228_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='private_code',
            field=models.BooleanField(default=False),
        ),
    ]
