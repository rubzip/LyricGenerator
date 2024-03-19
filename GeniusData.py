import os
import lyricsgenius 
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")
CLIENT_ACCESS_TOKEN = os.getenv("client_access_token")

genius = lyricsgenius.Genius(CLIENT_ACCESS_TOKEN)


