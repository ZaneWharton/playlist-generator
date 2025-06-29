#Run the server: uvicorn main:app --reload

import os
import httpx
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, Request, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, JSONResponse
from backend.auth import oauth, get_current_user
from backend.spotify import search_playlist
from dotenv import load_dotenv

app = FastAPI(title="Mood Playlist Generator")
load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Session middleware for user sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    same_site = "none",
    https_only=True,
    max_age=3600,  
)

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,
)

class SaveRequest(BaseModel):
    name: str
    description: str
    uris: List[str]

@app.get("/api/playlist")
async def get_playlist(mood: str, user=Depends(get_current_user)):
    #Generates a playlist based on the user's mood.
    
    playlist = await search_playlist(mood)
    if not playlist:
        raise HTTPException(status_code=404, detail="No playlist found for this mood")
    return {"playlist": playlist}

@app.post("/api/playlist/save")
async def save_playlist( request: Request, user=Depends(get_current_user), payload: SaveRequest = Body(...)):
    #Saves the generated playlist to the user's Spotify account.
    
    access_token = request.session.get('access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail="User not authenticated")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    create_playlist_url = f"https://api.spotify.com/v1/me/playlists"
    create_body = {
        "name": payload.name,
        "description": payload.description,
        "public": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(create_playlist_url, headers=headers, json=create_body)
        response.raise_for_status()
        created = response.json()
        
    playlist_id = created['id']

    add_tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    async with httpx.AsyncClient() as client:
        response = await client.post(add_tracks_url, headers=headers, json={"uris": payload.uris})
        response.raise_for_status()

    return {"url": f"https://open.spotify.com/playlist/{playlist_id}"}

@app.get("/auth/login")
async def login(request: Request):
    #Redirects the user to the Spotify login page.
   
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    return await oauth.spotify.authorize_redirect(request, redirect_uri=redirect_uri)

@app.get("/auth/callback")
async def callback(request: Request):
    #Handles the Spotify OAuth callback and retrieves the access token.

    token = await oauth.spotify.authorize_access_token(request) 
    user = await oauth.spotify.get('https://api.spotify.com/v1/me', token=token)
    access_token = token['access_token']
    request.session['user'] = user.json()
    request.session['access_token'] = token['access_token']
    return RedirectResponse(f"{FRONTEND_URL}/#access_token={access_token}")

@app.post("/auth/logout")
async def logout(request: Request):
    #Logs the user out by clearing the session.
    
    request.session.clear()
    return JSONResponse({"detail": "Logged out"})

static_directory = os.path.join(os.path.dirname(__file__), "../frontend/build")
app.mount("/", StaticFiles(directory=static_directory, html=True), name="static")