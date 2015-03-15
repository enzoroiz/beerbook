# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerbookapp', '0005_beer_avgrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='avgrating',
            field=models.IntegerField(default=0),
        ),
    ]
