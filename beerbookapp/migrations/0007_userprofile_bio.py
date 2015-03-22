# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beerbookapp', '0006_auto_20150319_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
