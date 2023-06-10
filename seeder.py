import json
import requests
from finglish import f2p

base_url = 'http://127.0.0.1:8000/seeder'

def divide_chunks(l, n):

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def seedArtist():
  with open("artists_details.json", "r") as f:
    artists = json.load(f)
    
  # for i in range(len(artists)):
  #   artists[i]['faName'] = f2p(artists[i]['name'])
    
  # with open("artists_details.json", "w") as f:
  #   json.dump(artists,f)
  
  chunked_artists = list(divide_chunks(artists, 20))
  # print(chunked_artists[1])
  # for i in chunked_artists:
  #   print(i)
  for artist in chunked_artists:
    # print(artist)
    res = requests.post(base_url+'/artists', json=artist)
    print(res.status_code)
  
def seedMusic():
  with open("processed_songs_465.local.json", "r") as f:
    musics = json.load(f)
  
  # for i in range(len(musics)):
  #   musics[i]['faName'] = f2p(musics[i]['name'])
  #   musics[i]['faTitle'] = f2p(musics[i]['title'])
    
  # with open("processed_songs_465.local.json", "w") as f:
  #   json.dump(musics, f)
  
  chunked_musics = list(divide_chunks(musics, 10))
  # print(chunked_musics[1])
  # return
  # for i in chunked_artists:
  #   print(i)
  for music in chunked_musics:
    # print(artist)
    res = requests.post(base_url+'/songs', json=music)
    print(res.status_code)
    if res.status_code != 201:
      ch_mus = list(divide_chunks(music, 5))
      for mu in ch_mus:
        res = requests.post(base_url+'/songs', json=mu)
        print('nested:',res.status_code)

if __name__ == '__main__':
  seedArtist()
  seedMusic()
