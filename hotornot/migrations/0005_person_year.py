# Generated by Django 3.1.7 on 2021-07-19 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotornot', '0004_person_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='year',
            field=models.SmallIntegerField(null=True),
        ),
    ]
