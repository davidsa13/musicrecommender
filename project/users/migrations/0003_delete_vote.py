# Generated by Django 3.0.5 on 2020-04-28 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_vote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
