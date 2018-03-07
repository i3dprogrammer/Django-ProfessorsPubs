# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 16:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]