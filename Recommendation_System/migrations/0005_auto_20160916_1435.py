# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Recommendation_System', '0004_auto_20160916_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='star_cast',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
