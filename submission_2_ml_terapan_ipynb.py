# -*- coding: utf-8 -*-
"""Submission 2 ML - Terapan.ipynb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D5xhal0iGmei47RU9f_LJN5nd6YkFTvN
"""

! chmod 600 /content/kaggle.json

! KAGGLE_CONFIG_DIR=/content/ kaggle datasets download -d grouplens/movielens-20m-dataset

"""## Data Preparation"""

import zipfile
zip_file = zipfile.ZipFile('/content/movielens-20m-dataset.zip')
zip_file.extractall('/tmp/')

"""### Import all realated libraries"""

# import libraries for data analysis
import numpy as np
import pandas as pd
import random
import os

# import library for visualization
import seaborn as sns
import matplotlib.pyplot as plt

"""### Import Dataset"""

rating=pd.read_csv('/tmp/rating.csv')
movies=pd.read_csv('/tmp/movie.csv')

print('Jumlah data rating oleh user: ', rating.shape[0])
print('Jumlah data informasi film: ', len(movies.movieId.unique()))

"""# EDA"""

rating.info()

rating['timestamp'] = pd.to_datetime(rating['timestamp'])
rating.sort_values(by='timestamp', ascending=False)

"""### Cek Unique setiap kolom rating"""

for col in rating.columns:
    c = rating[col].nunique()
    print(f"Unique count of {col} is {c}")

rating.drop(columns=['timestamp'],inplace=True)

rating.isnull().sum()

movies.info()

for col in movies.columns:
    c = movies[col].nunique()
    print(f"Unique count of {col} is {c}")

movies.isnull().sum()

movies.shape

movies

"""## Data Processing

### Menentukan user yang melakukan lebih dari 2000 kali memberikan rating (Downsampling)
"""

x=rating['userId'].value_counts() > 2000
y = x[x].index
y.shape

rating=rating[rating['userId'].isin(y)]
rating.shape

"""### Dataframe Rating merge dengan Dataframe movie_details"""

movie_details=movies.merge(rating,on='movieId')

movie_details.head()

movie_details.shape

"""### Mencari rank dari rating"""

number_rating = movie_details.groupby('title')['rating'].count().reset_index()

number_rating.rename(columns={'rating':'rank of rating'},inplace=True)

number_rating.head()

df=movie_details.merge(number_rating,on='title')

df.shape

df.sort_values(by='rank of rating', ascending=True)

"""### Memilih rank rating >= 50"""

df=df[df['rank of rating']<=50]

df.drop_duplicates(['title','userId'],inplace=True)

df.shape

df.head()

df.drop(columns=['rank of rating'],inplace=True)

df.head()

movie_pivot=df.pivot_table(columns='userId',index='title',values='rating')

movie_pivot.shape

movie_pivot.fillna(0,inplace=True)

movie_pivot

"""### Membuat variabel preparation yang berisi dataframe movie kemudian mengurutkan berdasarkan movieId"""

preparation = df
preparation.sort_values('movieId')

preparation.head()

import seaborn as sns
cmap=sns.diverging_palette(150,75,  s=40, l=65, n=9)
corrmat = preparation.corr()
plt.subplots(figsize=(12,12))
sns.heatmap(corrmat,cmap=cmap,annot=True, square=True);

"""### Model Development (Encoding)"""

# Mengubah userID menjadi list tanpa nilai yang sama
user_ids = preparation['userId'].unique().tolist()
print('list userID: ', user_ids)
 
# Melakukan encoding userID
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
print('encoded userID : ', user_to_user_encoded)
 
# Melakukan proses encoding angka ke ke userID
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
print('encoded angka ke userID: ', user_encoded_to_user)

# Mengubah movieId menjadi list tanpa nilai yang sama
movie_ids = preparation['movieId'].unique().tolist()
 
# Melakukan proses encoding movieId
movie_to_movie_encoded = {x: i for i, x in enumerate(movie_ids)}
 
# Melakukan proses encoding angka ke movieId
movie_encoded_to_movie = {i: x for i, x in enumerate(movie_ids)}

# Mapping userID ke dataframe user
preparation['user'] = preparation['userId'].map(user_to_user_encoded)
 
# Mapping movieID ke dataframe movie
preparation['movie'] = preparation['movieId'].map(movie_to_movie_encoded)

# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)
 
# Mendapatkan jumlah movie
num_movie = len(movie_to_movie_encoded)
print(num_movie)
 
# Mengubah rating menjadi nilai float
preparation['rating'] = preparation['rating'].values.astype(np.float32)
 
# Nilai minimum rating
min_rating = min(preparation['rating'])
 
# Nilai maksimal rating
max_rating = max(preparation['rating'])
 
print('Number of User: {}, Number of movie: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_movie, min_rating, max_rating
))

"""### Membagi Data untuk Training dan Validasi"""

# Mengacak dataset
df = df.sample(frac=1, random_state=42)
df

# Membuat variabel x untuk mencocokkan data user dan movie menjadi satu value
x = df[['user', 'movie']].values
 
# Membuat variabel y untuk membuat rating dari hasil 
y = df['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
 
# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)
 
print(x, y)

"""### Membuat model rekomendasi collaborative filtering"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path

class RecommenderNet(tf.keras.Model):
 
  # Insialisasi fungsi
  def __init__(self, num_users, num_movie, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_movie = num_movie
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.movie_embedding = layers.Embedding( # layer embeddings movie
        num_movie,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.movie_bias = layers.Embedding(num_movie, 1) # layer embedding movie bias
 
  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    movie_vector = self.movie_embedding(inputs[:, 1]) # memanggil layer embedding 3
    movie_bias = self.movie_bias(inputs[:, 1]) # memanggil layer embedding 4
 
    dot_user_movie = tf.tensordot(user_vector, movie_vector, 2) 
 
    x = dot_user_movie + user_bias + movie_bias
    
    return tf.nn.sigmoid(x)

"""### Inisialisasi model"""

model = RecommenderNet(num_users, num_movie, 50) 
 
# model compile
model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

"""### Memulai training"""

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 8,
    epochs = 20,
    validation_data = (x_val, y_val)
)

"""### Visualisasi training dan evaluation"""

import matplotlib.pyplot as plt
plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

movie_df = movies
 
# Mengambil sample user
user_id = df.userId.sample(1).iloc[0]
movie_watched_by_user = df[df.userId == user_id]
 
# Operator bitwise (~), bisa diketahui di sini https://docs.python.org/3/reference/expressions.html 
movie_not_watched = movie_df[~movie_df['movieId'].isin(movie_watched_by_user.movieId.values)]['movieId'] 
movie_not_watched = list(
    set(movie_not_watched)
    .intersection(set(movie_to_movie_encoded.keys()))
)
 
movie_not_watched = [[movie_to_movie_encoded.get(x)] for x in movie_not_watched]
user_encoder = user_to_user_encoded.get(user_id)
user_movie_array = np.hstack(
    ([[user_encoder]] * len(movie_not_watched), movie_not_watched)
)

movies.head()

"""### Mendapatkan rekomendasi film"""

# Mengambil sample user
user_id = df.userId.sample(1).iloc[0]
movie_watched_by_user = df[df.userId == user_id]
 
# Operator bitwise (~), bisa diketahui di sini https://docs.python.org/3/reference/expressions.html 
movie_not_watched = movie_df[~movie_df['movieId'].isin(movie_watched_by_user.movieId.values)]['movieId'] 
movie_not_watched = list(
    set(movie_not_watched)
    .intersection(set(movie_to_movie_encoded.keys()))
)
 
movie_not_watched = [[movie_to_movie_encoded.get(x)] for x in movie_not_watched]
user_encoder = user_to_user_encoded.get(user_id)
user_movie_array = np.hstack(
    ([[user_encoder]] * len(movie_not_watched), movie_not_watched)
)

ratings = model.predict(user_movie_array).flatten()
 
top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_movie_ids = [
    movie_encoded_to_movie.get(movie_not_watched[x][0]) for x in top_ratings_indices
]
 
print('Showing recommendations for users: {}'.format(user_id))
print('===' * 9)
print('movie with high ratings from user')
print('----' * 8)
 
top_movie_user = (
    movie_watched_by_user.sort_values(
        by = 'rating',
        ascending=False
    )
    .head(5)
    .movieId.values
)
 
movie_df_rows = movie_df[movie_df['movieId'].isin(top_movie_user)]
for row in movie_df_rows.itertuples():
    print(row.title, ':', row.genres)
 
print('----' * 8)
print('Top 10 movie recommendation')
print('----' * 8)
 
recommended_movie = movie_df[movie_df['movieId'].isin(recommended_movie_ids)]
for row in recommended_movie.itertuples():
    print(row.title, ':', row.genres)

