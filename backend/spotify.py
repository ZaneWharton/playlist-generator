#Spotify API integration for playlist generation based on user mood

import os
import time
import httpx
from dotenv import load_dotenv
import random
from fastapi import HTTPException

#Load environment variables from .env file
BASE = os.path.dirname(os.path.abspath(__file__))
DOTENV_FILE = os.path.join(BASE, ".env")

if os.path.exists(DOTENV_FILE):
    load_dotenv(dotenv_path=DOTENV_FILE)

#Credentials for Spotify API
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

#Constants for Spotify API
TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"

#Cache for access token to avoid frequent requests
token_cache = {}

#Function to get a valid access token from Spotify API.
async def get_token():
    now = int(time.time())

    #Check if the token is already cached and not expired
    if token_cache.get('expires_at', 0) > now + 60:
        return token_cache['access_token']
    
    #If token is expired or not cached, request a new one
    data = {'grant_type': 'client_credentials'}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
            response.raise_for_status()
            result = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching token: {e.response.text}")
    
    #Cache and return the new access token
    token_cache['access_token'] = result['access_token']
    token_cache['expires_at'] = now + result['expires_in']
    return token_cache['access_token']

#Function to search for a playlist based on the user's mood.
async def search_playlist(mood: str):
    #Searches for a playlist based on the user's mood using Spotify API. Randomly selects a genre based on the mood,
    #retrieves a random number of tracks (20-50) for that genre, and then fetches a set of tracks to create a playlist.

    token = await get_token()
    headers = {'Authorization': f'Bearer {token}'}

    #Mapping moods to genres
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

    #Pick random genre based on mood
    genres = genre_mapping.get(mood.lower(), ["pop"])
    genre = random.choice(genres)

    #Get total tracks count via a small search
    params_info = {'q': f'genre:"{genre}"', 'type': 'track', 'limit': 1}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SEARCH_URL, headers=headers, params=params_info)
            response.raise_for_status()
            info = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching genre info: {e.response.text}")
    
    total = info.get('tracks', {}).get('total', 0)
    #No tracks found for the genre
    if total == 0:
        raise HTTPException(status_code=404, detail=f"No tracks found for genre: {genre}")

    #Randomly select limit and offset for the search
    limit = random.randint(20, 50)  # Random limit between 20 and 50
    max_offset = min(total - limit, 10000) if total > limit else 0
    offset = random.randint(0, max_offset) if max_offset > 0 else 0

    #Call Spotify recommendations endpoint with correct params
    params = {'q': f'genre:"{genre}"', 'type': 'track', 'limit': limit, 'offset': offset}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SEARCH_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching tracks: {e.response.text}")

    #Return a structured response with the tracks
    return {
        "id": None,
        "name": f"{mood.capitalize()} Recommendations",
        "description": f"A random set of {limit} {mood}-mood tracks.",
        "url": None,
        "image": None,
        "tracks": data.get('tracks', []),
    }
