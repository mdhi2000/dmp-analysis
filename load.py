import json
from itertools import islice

def main_lyrics():
  _songs = {}
  with open("songs.local.json", "r") as f:
    _songs = json.load(f)
  
  print(len(_songs))
  
  print(json.dumps(_songs["1"],indent=4))
  
  with open("songs_lyric.local.json", "w") as fs:
    json.dump({k: v for k, v in _songs.items() if v['lyric'] != None}, fs)
  
def main():
  pass  

if __name__ == '__main__':
  main()