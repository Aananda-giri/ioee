# Generated by Django 3.2.6 on 2021-12-25 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_auto_20211225_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
