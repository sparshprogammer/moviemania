# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_friend', models.ForeignKey(related_name='friend_set', to=settings.AUTH_USER_MODEL)),
                ('to_friend', models.ForeignKey(related_name='to_friend_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friendship_Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friendship_status', models.IntegerField(default=0)),
                ('action_user', models.IntegerField()),
                ('request_from_friend', models.ForeignKey(related_name='request_friend_set', to=settings.AUTH_USER_MODEL)),
                ('request_to_friend', models.ForeignKey(related_name='request_to_friend_set', default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('year', models.PositiveIntegerField()),
                ('director', models.TextField(blank=True)),
                ('writer', models.TextField(blank=True)),
                ('star_cast', models.TextField(blank=True)),
                ('imdb_ratings', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('genres', models.CharField(max_length=200)),
                ('summary', models.TextField(blank=True)),
                ('length', models.PositiveIntegerField()),
                ('movie_img', models.ImageField(upload_to=b'movies_img', blank=True)),
                ('img', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status_update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=500)),
                ('posted_by', models.ForeignKey(related_name='Posted_by', to=settings.AUTH_USER_MODEL)),
                ('posted_to', models.ForeignKey(related_name='Posted_to', default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('date_of_birth', models.DateField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='friendship_request',
            unique_together=set([('request_from_friend', 'request_to_friend'), ('request_to_friend', 'request_from_friend')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('to_friend', 'from_friend')]),
        ),
    ]
