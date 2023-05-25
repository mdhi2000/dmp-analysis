import urllib.request
import json

def main():
  with open("./processed_songs_1000.local.json") as f:
    songs = json.load(f)
  
  print(songs[0])
  urllib.request.urlretrieve(songs[0]["hq_link"], "temp.mp3")

if __name__ == '__main__':
  main()