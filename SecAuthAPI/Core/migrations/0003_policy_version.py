# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_auto_20170802_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='version',
            field=models.SmallIntegerField(default=0),
        ),
    ]
