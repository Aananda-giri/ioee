# Generated by Django 3.1.7 on 2021-05-30 03:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hotornot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=50, null=True)),
                ('body', models.CharField(default=None, max_length=500)),
                ('loves', models.IntegerField(default=0)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
            ],
        ),
    ]
