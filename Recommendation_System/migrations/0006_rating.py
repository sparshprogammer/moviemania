# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-03 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Recommendation_System', '0005_auto_20160916_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movies_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Recommendation_System.Movie')),
            ],
        ),
    ]
