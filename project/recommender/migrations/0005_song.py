# Generated by Django 3.0.5 on 2020-04-26 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0004_popscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.TextField()),
                ('song', models.TextField()),
                ('mbtags', models.TextField()),
            ],
        ),
    ]
