# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-04 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_admins_loginsip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admins',
            name='phonenum',
            field=models.CharField(max_length=11),
        ),
    ]