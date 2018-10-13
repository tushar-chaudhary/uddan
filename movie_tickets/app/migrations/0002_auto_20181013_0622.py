# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-13 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie_details',
            name='aisle_seats',
        ),
        migrations.RemoveField(
            model_name='movie_details',
            name='number_of_seats',
        ),
        migrations.RemoveField(
            model_name='movie_details',
            name='row_name',
        ),
        migrations.AddField(
            model_name='movie_details',
            name='seatInfo',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]