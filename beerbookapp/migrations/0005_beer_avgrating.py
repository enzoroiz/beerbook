# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerbookapp', '0004_pub_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='avgrating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
