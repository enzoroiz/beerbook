# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField()),
                ('introduced', models.DateField()),
                ('image', models.ImageField(upload_to=b'beer_images', blank=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BeerProducer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BeerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('datetime', models.DateTimeField()),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FriendListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_one', models.ForeignKey(related_name=b'friend_one', to=settings.AUTH_USER_MODEL)),
                ('user_two', models.ForeignKey(related_name=b'friend_two', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('latitude', models.DecimalField(max_digits=5, decimal_places=3)),
                ('longitude', models.DecimalField(max_digits=5, decimal_places=3)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.ForeignKey(to='beerbookapp.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('established', models.DateField()),
                ('image', models.ImageField(upload_to=b'pub_images', blank=True)),
                ('location', models.ForeignKey(to='beerbookapp.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PubStockItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('stocked_at', models.ForeignKey(to='beerbookapp.Pub')),
                ('stocked_item', models.ForeignKey(to='beerbookapp.Beer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(default=0)),
                ('review', models.TextField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('rated_beer', models.ForeignKey(to='beerbookapp.Beer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('owner', 'rated_beer')]),
        ),
        migrations.AlterUniqueTogether(
            name='pubstockitem',
            unique_together=set([('stocked_item', 'stocked_at')]),
        ),
        migrations.AlterUniqueTogether(
            name='pub',
            unique_together=set([('name', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('latitude', 'longitude')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendlistitem',
            unique_together=set([('user_one', 'user_two')]),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(to='beerbookapp.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beer',
            name='producer',
            field=models.ForeignKey(to='beerbookapp.BeerProducer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beer',
            name='type',
            field=models.ForeignKey(to='beerbookapp.BeerType'),
            preserve_default=True,
        ),
    ]
