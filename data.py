from radiojavanapi import Client
import json

_songs = {}
_artists = []
songs_to_get = []


def get_song(song, extend=True):
    if song.id not in _songs:
        s = {
            "id": song.id,
            "name": song.name if hasattr(song, "name") else "",
            "artist": song.artist if hasattr(song, "artist") else "",
            "artist_tags": song.artist_tags if hasattr(song, "artist_tags") else "",
            "plays": song.plays if hasattr(song, "plays") else 0,
            "downloads": song.downloads if hasattr(song, "downloads") else 0,
            "created_at": song.created_at if hasattr(song, "created_at") else "",
            "permlink": song.permlink if hasattr(song, "permlink") else "",
            "photo": song.photo if hasattr(song, "photo") else "",
            "photo_player": song.photo_player if hasattr(song, "photo_player") else "",
            "share_link": song.share_link if hasattr(song, "share_link") else "",
            "title": song.title if hasattr(song, "title") else "",
            "credits": song.credits if hasattr(song, "credits") else "",
            "credit_tags": song.credit_tags if hasattr(song, "credit_tags") else "",
            "likes": song.likes if hasattr(song, "likes") else 0,
            "dislikes": song.dislikes if hasattr(song, "dislikes") else 0,
            "link": song.link if hasattr(song, "link") else "",
            "hq_link": song.hq_link if hasattr(song, "hq_link") else "",
            "lq_link": song.lq_link if hasattr(song, "lq_link") else "",
            "hls_link": song.hls_link if hasattr(song, "hls_link") else "",
            "hq_hls": song.hq_hls if hasattr(song, "hq_hls") else "",
            "lq_hls": song.lq_hls if hasattr(song, "lq_hls") else "",
            "album": song.album if hasattr(song, "album") else "",
            "date": song.date if hasattr(song, "date") else "",
            "duration": song.duration if hasattr(song, "duration") else 0,
            "thumbnail": song.thumbnail if hasattr(song, "thumbnail") else "",
            "lyric": song.lyric if hasattr(song, "lyric") else "",
        }
        _songs[song.id] = s
    if extend:
        _artists.append(song.artist)
        for s in song.related_songs:
            if s.id not in _songs:
                songs_to_get.append(s.id)
                if hasattr(s, "artist") and s.artist not in _artists:
                    _artists.append(s.artist)
    return (_songs, _artists, songs_to_get)


def load(name):
    try:
        with open(name + ".json", "r") as f:
            s = json.load(f)
            j = s if isinstance(s, dict) else {}
    except:
        j = {}
    return j


def save(j, name):
    with open(name + ".json", "w") as f:
        json.dump(j, f)


def main():
    _songs = load("songs")
    _artists = load("artists")
    # Create a Client instance and get a song info.
    client = Client()
    # song = client.get_song_by_url(
    #     'https://www.radiojavan.com/mp3s/mp3/Sijal-Baz-Mirim-Baham-(Ft-Sami-Low)')

    # print(f"""
    #         Name: {song.name}
    #         Artist: {song.artist}
    #         HQ-Link: {song.hq_link}
    # """)

    # print("Trending Song:\n\n")

    songs = client.get_trending_songs()

    for song in songs:
        (_songs, _artists, songs_to_get) = get_song(song)
        print(song.name)

    print()

    # return print(songs[1])

    print("Popular Song:\n\n")

    songs = client.get_popular_songs()

    for song in songs:
        (_songs, _artists, songs_to_get) = get_song(song)
        print(song.name)

    print()

    print("Featured Song:\n\n")

    songs = client.get_featured_songs()

    for song in songs:
        (_songs, _artists, songs_to_get) = get_song(song)
        print(song.name)

    print()

    print("Latest albums:\n\n")

    albums = client.get_latest_albums()

    for album in albums:
        for song in album.tracks:
            (_songs, _artists, songs_to_get) = get_song(song)
        print(album.name)

    print()

    print("Artists:\n\n")
    print(_artists, len(_artists))
    print()

    for a in set(_artists):
        try:
            artist = client.get_artist_by_name(a)
            for song in artist.songs:
                if song.id not in _songs:
                    songs_to_get.append(song.id)
        except:
            pass

    dept = 0

    while dept <= 10:
        temp = songs_to_get
        songs_to_get = []
        print(temp, len(temp))
        for s in set(temp):
            print(s)
            song = client.get_song_by_id(s)
            (_songs, _artists, songs_to_get) = get_song(song)

        dept += 1

    save(_songs, 'songs')
    save(set(_artists), 'artists')

    print()
    print("songs collected: ", len(_songs))


def main2():
    _songs = load("songs")
    # _artists = load("artists")
    client = Client()

    for i in range(127000):
        # print(i)
        try:
            if i not in _songs:
                song = client.get_song_by_id(i)
                (_songs, _artists, songs_to_get) = get_song(song)
        except:
            # print("NotFound")
            pass
        if i % 100 == 0:
            save(_songs, f"songs.local")
            print("Saved.i: ", i, " ,count: ", len(_songs))
    save(_songs, 'songs')

    print()
    print("songs collected: ", len(_songs))


def get_artists():
    client = Client()
    with open('songs.local.json', 'r') as f:
        songs = json.load(f)

    artists = []
    for song in songs.values():
        artists.append(song['artist'])

    print(len(set(artists)), len(artists))

    artists_details = []

    # for i in range(3000,3005):
    #     artist = artists[i]
    for artist in set(artists):
        print(artist)
        artist_details = client.get_artist_by_name(artist)
        temp = {
            "name": artist_details.name if hasattr(artist_details, "name") else "",
            "plays": artist_details.plays if hasattr(artist_details, "plays") else "",
            "photo": artist_details.photo if hasattr(artist_details, "photo") else "",
            "photo_player": artist_details.photo_player if hasattr(artist_details, "photo_player") else "",
            "photo_thumb": artist_details.photo_thumb if hasattr(artist_details, "photo_thumb") else "",
            "background": artist_details.background if hasattr(artist_details, "background") else "",
            "share_link": artist_details.share_link if hasattr(artist_details, "share_link") else "",
            "following": artist_details.following if hasattr(artist_details, "following") else "",
            "followers_count": artist_details.followers_count if hasattr(artist_details, "followers_count") else "",
            "prerelease": artist_details.prerelease if hasattr(artist_details, "prerelease") else [],
            "photos": artist_details.photos if hasattr(artist_details, "photos") else [],
            "events": artist_details.events if hasattr(artist_details, "events") else [],
        }
        artists_details.append(temp)
      # except Exception as e:
            # print("Error: ", str(e))
    with open("artists_details.json", "w") as f:
        json.dump(artists_details, f)


if __name__ == "__main__":
    # main2()
    get_artists()
