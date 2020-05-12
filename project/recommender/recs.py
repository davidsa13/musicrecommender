from .models import Song
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import django_pandas.io as sql


#Class for Popularity based Recommender System model
class popularity_rec():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.popularity_recommendations = None
        
    #Create the popularity based recommender system model
    def create(self, train_data, user_id, song):
        self.train_data = train_data
        self.user_id = user_id
        self.song = song

        #Get a count of user_ids for each unique song as recommendation score
        train_grouped = train_data.groupby([self.song]).agg({self.user_id: 'count'}).reset_index()
        train_grouped.rename(columns = {self.user_id: 'score'},inplace=True)
    
        #Sort the songs based upon recommendation score
        train_sort = train_grouped.sort_values(['score', self.song], ascending = [0,1])
    
        #Generate a recommendation rank based upon score
        train_sort['Rank'] = train_sort['score'].rank(ascending=0, method='first')
        
        #Get the top 10
        self.popularity_recommendations = train_data_sort.head(10)

    
    #make recommendations
    def recommend(self, user_id):    
        user_recommendations = self.popularity_recommendations
        cols = user_recommendations.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        user_recommendations = user_recommendations[cols]
        
        return user_recommendations

class content_rec:
    def __init__(self):
        self.cosine_sim= None
        self.indices = None
        self.df= None

    def create(self):
        song = Song.objects.all()
        df = sql.read_frame(song)
        df2 = df.drop(['id','song_id'], axis=1)
        df2.set_index('song', inplace=True)
        count = CountVectorizer()
        count_matrix = count.fit_transform(df2['mbtags'])
        self. indices = pd.Series(df2.index)
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)
        self.df =df2

    
    def recommend(self, song):
        cosine_sim = self.cosine_sim
        indices = self.indices
        df = self.df
        recommended_songs = []
        idx=indices[indices== song].index[0]
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

        top_10_indexes = list(score_series.iloc[1:11].index)

        for i in top_10_indexes:
            recommended_songs.append(list(df.index)[i])

        return recommended_songs
'''
songs = Post.objects.all()
df = sql.read_frame(songs)
df['song'] = df['title'].map(str) + "-" + df['artist_name']
df_subset = df.head(10000)
song_grouped = df_subset.groupby(['song']).agg({'listen_time':'count'}).reset_index()
grouped_sum = song_grouped['listen_time'].sum()
song_grouped['percentage'] = song_grouped['listen_time'].div(grouped_sum) *100
sort_songs = song_grouped.sort_values(['listen_time','song'], ascending =[0,1])
users = df['listener'].unique()
songs = df['song'].unique()
train_data, test_data = train_test_split(df, test_size =0.20, random_state= 0)
pm = popularity_rec()
pm.create(train_data,'listener','song')
user_id = users[5]
a = pm.recommend(user_id)
'''