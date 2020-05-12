# Generated by Django 3.0.5 on 2020-04-28 10:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommender', '0006_popscore_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='likes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]