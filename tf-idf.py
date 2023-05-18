import json
from hazm import *
from hazm.utils import stopwords_list

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

import pandas as pd
import numpy as np

from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt


stopwords = stopwords_list()

counter = 0

def preprocess(text):
  global counter
  print(counter)
  print()
  print(text)
  print()
  counter += 1
  
  text = Normalizer().normalize(text)
  sentences = SentenceTokenizer().tokenize(text)
  # print("sentences: ",sentences)
  words = sum((WordTokenizer().tokenize(sentence) for sentence in sentences),[])
  # print("words: ",words)
  temp = []
  for word in words:
    if word not in stopwords:
      temp.append(word)
  word_lems = [Lemmatizer().lemmatize(word) for word in temp]
  # print("word_lems: ",word_lems)
  return word_lems
  

# def get_top_keywords(n_terms):
#     """This function returns the keywords for each centroid of the KMeans"""
#     df = pd.DataFrame(X.todense()).groupby(
#         clusters).mean()  # groups the TF-IDF vector by cluster
#     terms = vectorizer.get_feature_names_out()  # access tf-idf terms
#     for i, r in df.iterrows():
#         print('\nCluster {}'.format(i))
#         # for each row of the dataframe, find the n terms that have the highest tf idf score
#         print(','.join([terms[t] for t in np.argsort(r)[-n_terms:]]))


# get_top_keywords(10)

def main():
  with open('./songs_lyric.local.json') as slf:
    songs_lyric = json.load(slf)
    
  songs_lyric_array = list(songs_lyric.values())
  
  df = pd.DataFrame(songs_lyric_array, columns=['lyric'])
  
  df['cleaned'] = df['lyric'].apply(lambda x: preprocess(x))
  
  # lyrics = []
  
  # # preprocess(songs_lyric_array[0]['lyric'])
  # for lyric in songs_lyric_array:
  #   lyrics.append(preprocess(lyric))
    
  vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, max_df=0.95)
  X = vectorizer.fit_transform(df['cleaned'])
  
  kmeans = KMeans(n_clusters=10, random_state=42)
  
  dbscan = DBSCAN(min_samples=20)


  kmeans.fit(X)
  clusters = kmeans.labels_
  
  for i in range(len(songs_lyric_array)):
    songs_lyric_array[i]['kmeans_label'] = clusters[i]
  
  with open('./processed_songs.local.json') as f:
    json.dump(songs_lyric_array, f)
  
  print(kmeans.cluster_centers_)

def eps():
  with open('./songs_lyric.local.json') as slf:
    songs_lyric = json.load(slf)

  songs_lyric_array = list(songs_lyric.values())

  df = pd.DataFrame(songs_lyric_array, columns=['lyric'])
  neighbors = NearestNeighbors(n_neighbors=20)
  neighbors_fit = neighbors.fit(df['lyric'])
  distances, indices = neighbors_fit.kneighbors(df['lyric'])
  
  distances = np.sort(distances, axis=0)

  distances = distances[:, 1]
  plt.plot(distances)
  
def dump_dataframe():
  with open('./songs_lyric.local.json') as slf:
    songs_lyric = json.load(slf)

  songs_lyric_array = list(songs_lyric.values())

  df = pd.DataFrame(songs_lyric_array, columns=['lyric'])

  df['cleaned'] = df['lyric'].apply(lambda x: preprocess(x))
  
  df.to_pickle('songs_lyrics.pkl')
  

if __name__ == '__main__':
  dump_dataframe()
