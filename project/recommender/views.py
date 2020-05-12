from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, PopScore
from .recs import popularity_rec

import django_pandas.io as sql
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split



# Create your views here.
posts = [
    {
        'content': 'Music For Everyone'
    }
]

def home(request):
    context = {
        #'posts': posts
        

    }
    return render(request, 'recommender/home.html', context)

