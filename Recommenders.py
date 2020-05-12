import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class popularity_rec():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.song = None
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
        self.popularity_recommendations = train_sort.head(10)

    
    #make recommendations
    def recommend(self, user_id):    
        user_recommendations = self.popularity_recommendations
        cols = user_recommendations.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        user_recommendations = user_recommendations[cols]
        
        return user_recommendations
        
class collab_rec():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.song_id = None
        self.title = None
        self.artist = None
        self.cooccurrence_matrix = None
        
    def get_user_songs(self, user):
        user_data = self.train_data[self.train_data[self.user_id] == user]
        user_songs= list(user_data[self.song_id].unique())
        
        return  user_songs
    
    def get_song_users(self,song_id):
        song_data = self.train_data[self.train_data[self.song_id]==song_id]
        song_users = set(song_data[self.user_id].unique())

        return song_users

    def get_all_songs_train_data(self):
        all_songs_id = list(self.train_data[self.song_id].unique())

        return all_songs_id

    def get_title(self):
        all_songs_title = list(self.train_data[self.title].unique())

        return all_songs_title
    
    def get_artist_name(self):
        all_songs_artist_name = list

    
    def create(self, train_data, user_id, song_id, title, artist_name):
        self.train_data = train_data
        self.user_id = user_id
        self.song_id = song_id
        self.title = title
        self.artist = artist_name
    

    def construct_cooccurrence_matrix(self,user_songs, all_songs):

        user_songs_users = []
        for i in range(0, len(user_songs)):
            user_songs_users.append(self.get_song_users(user_songs[i]))

        cooccurrence_matrix = np.matrix(np.zeros(shape=(len(user_songs), len(all_songs))), float)

        for i in range(0,len(all_songs)):
            songs_i_data = self.train_data[self.train_data[self.song_id] == all_songs[i]]
            users_i = set(songs_i_data[self.user_id].unique())

            for j in range(0,len(user_songs)):

                users_j = user_songs_users[j]

                users_intersection = users_i.intersection(users_j)

                if len(users_intersection) != 0:
                    users_union = users_i.union(users_j)

                    cooccurrence_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
                else:
                    cooccurrence_matrix[j,i] = 0

        return cooccurrence_matrix            

    def generate_top_recommendation(self, user, cooccurrence_matrix, all_songs, user_songs):

        user_sim_scores = cooccurrence_matrix.sum(axis=0)/float(cooccurrence_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()

        sort_index =sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)

        columns = ['title', 'artist_name','song_id', 'score', 'rank']
        df = pd.DataFrame(columns = columns)

        rank=1
        for i in range(0, len(sort_index)):
            if ~np.isnan(sort_index[i][0]) and all_songs[sort_index[i][1]] not in user_songs and rank <= 10:
                title_data = list(self.train_data.loc[self.train_data[self.song_id]== all_songs[sort_index[i][1]],'title'])
                artist_name_data = list(self.train_data.loc[self.train_data[self.song_id]== all_songs[sort_index[i][1]],'artist_name'])
                df.loc[len(df)] = [title_data[0], artist_name_data[0], all_songs[sort_index[i][1]], sort_index[i][0], rank]
                rank = rank+1
        
        if df.shape[0] == 0:
            print('The current user has no songs for training the item similarity based recommendation model.')
            return -1
        else:
            return df

    def recommend(self,user):
        # Get all unique songs for target user
        user_songs = self.get_user_songs(user)

        #Get all unique songs in the training data
        all_songs = self.get_all_songs_train_data()

        # Construct item cooccurence matrix 
        cooccurrence_matrix = self.construct_cooccurrence_matrix(user_songs, all_songs)

        df_recommendations = self.generate_top_recommendation(user, cooccurrence_matrix, all_songs, user_songs)

        return df_recommendations

    


class content_rec:
    def __init__(self):
        self.cosine_sim= None
        self.indices = None
        self.df = None

    def create(self, df):
        self.df = df
        count = CountVectorizer()
        count_matrix = count.fit_transform(self.df['mbtag'])
        self. indices = pd.Series(self.df.index)
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)


    
    def recommend(self, song):
        cosine_sim = self.cosine_sim
        indices = self.indices
        df = self.df
        
        idx=indices[indices== song].index[0]
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

        top_10_indexes = list(score_series.iloc[1:11].index)

        columns = ['song']
        recommend_songs = pd.DataFrame(columns = columns)

        for i in top_10_indexes:
            recommend_songs.loc[len(recommend_songs)]= df.index[i]

        return recommend_songs
