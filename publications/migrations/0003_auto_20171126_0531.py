# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_publication_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.IntegerField(default=0),
        ),
    ]
