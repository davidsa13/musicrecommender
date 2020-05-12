from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    song_id = models.TextField()
    title = models.TextField()
    artist_id = models.TextField()
    artist_name = models.TextField()
    listener= models.TextField(default = 'some string')
    listen_time = models.TextField()

    def __str__(self):
        return self.title


class PopScore(models.Model):
    Rank = models.IntegerField()
    Song = models.TextField()
    Score = models.IntegerField()
    likes = models.ManyToManyField(User)

    def __str__(self):
        return self.Song

class Song(models.Model):
    song_id = models.TextField()
    song = models.TextField()
    mbtags = models.TextField()
    likes = models.ManyToManyField(User)

