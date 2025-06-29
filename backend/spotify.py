import os
import time
import httpx
from dotenv import load_dotenv
import random

load_dotenv()

# Constants for Spotify API
TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"

# Credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


token_cache = {}

async def get_token():
    now = int(time.time())
    if token_cache.get('expires_at', 0) > now + 60:
        return token_cache['access_token']
    data = {'grant_type': 'client_credentials'}
    async with httpx.AsyncClient() as client:
        resp = await client.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
        resp.raise_for_status()
        result = resp.json()
    token_cache['access_token'] = result['access_token']
    token_cache['expires_at'] = now + result['expires_in']
    return token_cache['access_token']

async def search_playlist(mood: str):
    # Searches for a playlist based on the user's mood using Spotify API.

    token = await get_token()
    headers = {'Authorization': f'Bearer {token}'}

    genre_mapping = {
        'happy': ['pop', 'dance', 'disco', 'funk', 'electronic', 'house', 'dancehall'],
        'sad': ['acoustic', 'indie', 'indie-pop', 'singer-songwriter', 'piano', 'sad', 'ballad'],
        'energetic': ['rock', 'metal', 'edm', 'punk', 'hard-rock', 'hip-hop', 'drum-and-bass'],
        'chill': ['ambient', 'lo-fi', 'chill', 'downtempo', 'jazz', 'soul', 'new-age'],
        'romantic': ['romance', 'love', 'r-n-b', 'jazz', 'soul', 'acoustic', 'ballad'],
        'motivational': ['power-pop', 'uplifting', 'dance', 'edm', 'pop', 'rock'],
        'nostalgic': ['retro', 'classic', 'old-school', 'classic-rock'],
        'angry': ['punk', 'hardcore', 'metalcore', 'heavy-metal', 'emo', 'grunge'],
        'relaxed': ['jazz', 'blues', 'brazil', 'latin', 'reggae', 'instrumental', 'smooth-jazz'],
        'focused': ['classical', 'electronic', 'ambient', 'study', 'instrumental', 'minimal-techno'],
    }

    #Pick seed genres for recommendations
    genres = genre_mapping.get(mood.lower(), ["pop"])
    genre = random.choice(genres)

    #Get total tracks count via a small search
    params_info = {'q': f'genre:"{genre}"', 'type': 'track', 'limit': 1}
    async with httpx.AsyncClient() as client:
        resp_info = await client.get(SEARCH_URL, headers=headers, params=params_info)
        resp_info.raise_for_status()
        info = resp_info.json()
    total = info.get('tracks', {}).get('total', 0)

    limit = random.randint(20, 50)  # Random limit between 10 and 50
    max_offset = min(total - limit, 10000) if total > limit else 0
    offset = random.randint(0, max_offset) if max_offset > 0 else 0

    #Call Spotify recommendations endpoint with correct params
    params = {'q': f'genre:"{genre}"', 'type': 'track', 'limit': limit, 'offset': offset}
    async with httpx.AsyncClient() as client:
        print(f"Calling {SEARCH_URL} with {params}")
        resp = await client.get(SEARCH_URL, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

    return {
        "id": None,
        "name": f"{mood.capitalize()} Recommendations",
        "description": f"A random set of {limit} {mood}-mood tracks.",
        "url": None,
        "image": None,
        "tracks": data.get('tracks', []),
    }
