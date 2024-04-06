# LyricGenerator

The goal of this project is to apply all the knowledge acquired in "Applications 1" and develop a project. 
In this project we finetune an LLM to generate the lyrics of English pop songs. We create the dataset from scratch and provide the code to reproduce each of the steps we followed:

* [Data Extraction](src/01_Data_Extraction.ipynb) - we use Genius' API to download 10 songs from the top 100 pop artists of the moment.
* [Data Cleaning](src/02_Data_Cleaning.ipynb) - we preprocess and build our train, development and test datasets.
* [Flan Finetuning](src/03_FLAN_trainer.ipynb) - we use FLAN (small) to finetune our model and adapt it to song lyric generation.
* [T5 Finetuning](src/03_T5_trainer.ipynb) - we use T5 (small) to finetune our model and adapt it to song lyric generation.
* [GPT Finetuning](src/03_GPT_trainer.ipynb) - we use GPT 2 to finetune our model and adapt it to song lyric generation.
* [Metrics Evaluation](src/04_Metrics_Evaluation.ipynb) - we compute the BLEU score and the perplexity of our generated lyrics.
* [Mistral Evaluation](src/04_Mistral_Evaluation.ipynb) - we call Mistral's API to assess our results in terms of musicality, coherence and quality.


## 🚀 Reproducing Results

To reproduce the experiments and results, make sure you install all the dependencies by doing:

```console
pip install -r requirements.txt
```

### ✏️ Data Extraction

We didn't find any datasets valid for our task so we decided to build it from scratch.
Data was obtained from [Genius](https://genius.com/), if you want to reply our data extraction process you will need to obtain an API key and add `.env` file to the root folder.

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

After that, we selected the top 100 artists more listened in English from: [/main/data/100_artists_pop_english.csv](https://github.com/rubzip/LyricGenerator/blob/main/data/100_artists_pop_english.csv).
Using Genius' API we have scrapped the lyrics of the top 10 most famous songs of each artist.

```python
import lyricsgenius
import json 

genius = lyricsgenius.Genius(CLIENT_ACCESS_TOKEN)

# The next code scraps the top 3 songs of the weekend and stores data as a JSON file.
artist_name = "The weekend"

songs = get_songs(artist_name, n_songs=3)
with open(f"data/jsons/{artist_name.replace(' ', '_')}.json", 'w') as f:
    json.dump(songs, f)
```

## Data Cleaning
For each artist we have downloaded a JSON file that contains the top 10 songs in the folder `/main/data/jsons/`.
Songs are formatted in Genius API as: 
```
197 ContributorsTranslationsTürkçeEspañolPortuguêsΕλληνικάDeutschDusk Till Dawn Lyrics[Verse 1: ZAYN]
Not tryna be indie
Not tryna be cool
Just tryna be in this
Tell me, are you too?
Can you feel where the wind is?
Can you feel it through
All of the windows
Inside this room?

[Refrain: ZAYN]
'Cause I wanna touch you, baby
And I wanna feel you too
I wanna see the sun rise on your sins
Just me and you

[Pre-Chorus: ZAYN & Sia, Sia]
Light it up, on the run
Let's make love tonight
Make it up, fall in love, try
(Baby, I'm right here)
```

For making our model easier to train, we filtered non-lyrics text and we splitted songs by tags (`[Verse 1: ZAYN]`, `[Refrain: ZAYN]`, `[Pre-Chorus: ZAYN & Sia, Sia]`).
And after that we cleaned tags as simple as possible:
```
[Verse 1: ZAYN] -> [Verse]
[Refrain: ZAYN] -> [Refrain]
[Pre-Chorus: ZAYN & Sia, Sia] -> [Pre-Chorus]
```
Resulting dataframe as:
| artist              | song         | content                                                                                                                                                                                            | tag      |
|---------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| 5 Seconds of Summer | Ghost of You | Here I am waking up, still can't sleep on your side There's your coffee cup, the lipstick stain fades with time If I can dream long enough, you'd tell me I'd be just fine I'll be just fine       | [Verse]  |
| 5 Seconds of Summer | Ghost of You | So I drown it out like I always do Dancing through our house with the ghost of you And I chase it down, with a shot of truth Dancing through our house with the ghost of you                       | [Chorus] |
| 5 Seconds of Summer | Ghost of You | Cleanin' up today, found that old Zeppelin shirt You wore when you ran away, and no one could feel your hurt We're too young, too dumb, to know things like love But I know better now, better now | [Verse]  |

## Data Splitting
Once we have all our data correctly formated, we have splitted it to `train`, `val`, and `test`. For the `test` dataset we have selected a song per artist, so these songs are not avaliable in `train` nor `val`, and the rest of data has been randomly slitted into `train` and `val`.



