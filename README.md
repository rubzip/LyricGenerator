# LyricGenerator

The goal of this project is to apply all the knowledge acquired in "Applications 1", and develop a project.
In our case, we have decided to finetune a LLM to generate pop lyric songs. 

## Data Extraction

We didn't found any datasets valid for our task so we decided to build it from scratch.
Data was obtained from (Genius)[https://genius.com/], if you want to reply our data extraction process you will need to obtain an API key and add `.env` file to the `/main/` folder.

```
# .env file content:
client_id = XXXXXXXXXXXXXXXXXXXXX
client_secret = XXXXXXXXXXXXXXXXX
client_access_token = XXXXXXXXXXX
```

```python
# Loading API credentials:
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")
CLIENT_ACCESS_TOKEN = os.getenv("client_access_token")
```

After that we have selected the top 100 artist more listened in english from: (/main/data/100_artists_pop_english.csv)[https://github.com/rubzip/LyricGenerator/blob/main/data/100_artists_pop_english.csv].
Using Genius' API we have scrapped the lyrics of top 10 most famous songs of each artist.

```python
genius = lyricsgenius.Genius(CLIENT_ACCESS_TOKEN)

def get_songs(artist_name, n_songs=10, t_sleep=30):
    while True:
        try:
            artist = genius.search_artist(artist_name, max_songs=n_songs)
            songs = dict()
            for song in artist.songs:
                songs[song.title] = song.lyrics
            return songs
        except Exception as f:
            print(f)
            time.sleep(t_sleep)
```
