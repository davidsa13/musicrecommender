from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.contrib.auth.decorators import login_required
from django.db import models
from  recommender.models import Post, PopScore, Song
from .forms import UserRegisterForm
from recommender.recs import content_rec
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def like_post(request):
    post = get_object_or_404(PopScore, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect('/profilehome/')

def like_post2(request):
    post = get_object_or_404(Song, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect('/profilehome/')

def get_user(request):
    current_user = request.user.username
    return current_user


class profile():
    
    @login_required
    def setting(request):
        return render(request, 'users/profile.html')
    
    @login_required
    def profilehome(request):

        poprec=PopScore.objects.all()
        
        context = {
            'poprec': poprec,
        }

        return render(request, 'users/home.html', context)

    def personalize(request):
        current_user = request.user.id
        likespop = PopScore.likes.through.objects.all()
        music_data = Song.objects.all()
        
        # Get all users who like a song
        likesuser=[]
        for like in likespop:
            if like.user_id not in likesuser:
                likesuser.append(like.user_id)
        
        # Get all songs id like be current user
        song_id=[]
        for like in likespop:
            if like.user_id == current_user:
                song_id.append(like.popscore_id)
        
        popscore=PopScore.objects.all()
        song=[]
        for id in song_id:
            for i in popscore:
                if id == i.id:
                    song.append(i.Song)
        
        if len(song) == 0:
            poprec = PopScore.objects.all()
            df1 = []
        else:
            poprec = []
            firstsong = song[0]
            df=content_rec()
            df1= df.create()
            df1= df.recommend(firstsong)

        df_dic = {}
        for song in df1:
            for i in music_data:
                if song == i.song:
                    df_dic[song] = i.id
        


        context = {
            'poprec': poprec,
            'contentrec': df_dic,
            'likesuser' : likesuser,
        }

        return render(request, 'users/personalize.html', context)