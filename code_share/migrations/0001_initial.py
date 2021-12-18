# Generated by Django 3.2.6 on 2021-12-18 05:00

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.TextField()),
                ('author', models.CharField(default='', max_length=80)),
                ('email', models.EmailField(default='', max_length=254)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=150), default=None, null=True, size=None)),
                ('valid_email', models.BooleanField(default=True)),
                ('hide_code', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(default=None, max_length=50, null=True)),
                ('body', models.CharField(default=None, max_length=500)),
                ('loves', models.IntegerField(default=0)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='code_share.post')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
