# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import beerbookapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('beerbookapp', '0005_rating_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'profile_images/default.png', upload_to=beerbookapp.models.file_rename, blank=True),
        ),
    ]
