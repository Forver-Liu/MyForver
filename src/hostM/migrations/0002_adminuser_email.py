# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-17 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostM', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]