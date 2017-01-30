# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-27 06:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_room', '0003_slide'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='room',
            field=models.ForeignKey(default='test', on_delete=django.db.models.deletion.CASCADE, to='manage_room.Room'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slide',
            name='title',
            field=models.CharField(default='(empty)', max_length=35),
        ),
    ]