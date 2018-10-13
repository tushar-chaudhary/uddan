# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-13 07:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20181013_0623'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveSeats',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('screen_name', models.CharField(max_length=100)),
                ('seats', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Movie Reserve',
                'verbose_name_plural': 'Movie Reserves',
                'ordering': ['id'],
            },
        ),
    ]