# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Recommendation_System', '0003_auto_20160916_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='writer',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
