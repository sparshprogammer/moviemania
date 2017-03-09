# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Recommendation_System', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_ratings',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
