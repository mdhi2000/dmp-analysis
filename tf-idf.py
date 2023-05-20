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
  
  # df = pd.DataFrame(songs_lyric_array, columns=['lyric'])
  
  # df['cleaned'] = df['lyric'].apply(lambda x: preprocess(x))
  
  # lyrics = []
  
  # # preprocess(songs_lyric_array[0]['lyric'])
  # for lyric in songs_lyric_array:
  #   lyrics.append(preprocess(lyric))
  
  df = pd.read_pickle('songs_lyrics.pkl')
  
  print(df['cleaned'][0])
    
  vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, max_df=0.95)
  X = vectorizer.fit_transform(df['lyric'])
  
  kmeans = KMeans(n_clusters=465, random_state=42)
  
  dbscan = DBSCAN(5,min_samples=20)
  dbscan.fit(X)


  kmeans.fit(X)
  clusters = kmeans.labels_
  
  print(type(clusters[0]))
  print(type(dbscan.labels_[0]))
  
  for i in range(len(songs_lyric_array)):
    songs_lyric_array[i]['kmeans_label'] = int(clusters[i])
    songs_lyric_array[i]['dbscan_label'] = int(dbscan.labels_[i])
  
  with open('./processed_songs.local.json','w') as f:
    json.dump(songs_lyric_array, f)
  
  print(kmeans.cluster_centers_)

def eps():
  # with open('./songs_lyric.local.json') as slf:
  #   songs_lyric = json.load(slf)

  # songs_lyric_array = list(songs_lyric.values())

  # df = pd.DataFrame(songs_lyric_array, columns=['lyric'])
  df = pd.read_pickle('songs_lyrics.pkl')
  neighbors = NearestNeighbors(n_neighbors=20)
  neighbors_fit = neighbors.fit(df['cleaned'])
  distances, indices = neighbors_fit.kneighbors(df['cleaned'])
  
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
  
  


def check_json_file():
  with open('./processed_songs.local.json') as f:
    songs = json.load(f)
    
  sr = {}
  print('kmeans:\n')
  for song in songs:
    if song['kmeans_label'] not in sr:
      sr[song['kmeans_label']] = [
        song,
      ]
      
    else:
      sr[song['kmeans_label']].append(song)
      
  sr={}
  print('dbscan')
  for song in songs:
   
    if song['dbscan_label'] not in sr:
      sr[song['dbscan_label']] = [
        song,
      ]
      
    else:
      sr[song['dbscan_label']].append(song)
  
  # print(len(list(sr.values())))
  print(sr.keys())
  
  for i in list(sr.items())[:10]:
    print()
    print()   
    for song in i:
      print(type(song))
      print(song['name'], ', ', song['artist'])
    print(len(i))
      
  print(len(sr))

if __name__ == '__main__':
  main()
  check_json_file()
  # eps()