# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerbookapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beerproducer',
            name='name',
            field=models.CharField(unique=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='beertype',
            name='name',
            field=models.CharField(unique=True, max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('title', 'datetime')]),
        ),
    ]
