# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-10 18:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Recommendation_System', '0009_auto_20170107_2011'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('movies', 'user')]),
        ),
    ]
