#Mood Playlist Generator Backend
#Before running the server, ensure you have the required environment variables set in a .env file.
#Before running the server, install the required packages: pip install requirements.txt
#Before running the server, run npm install and npm run build in the frontend directory to build the React app.
#Run the server from root directory: uvicorn backend.main:app --reload 

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

#Load environment variables from .env file
BASE = os.path.dirname(os.path.abspath(__file__))
DOTENV_FILE = os.path.join(BASE, ".env")

if os.path.exists(DOTENV_FILE):
    load_dotenv(dotenv_path=DOTENV_FILE)

#Initialize FastAPI application
app = FastAPI(title="Mood Playlist Generator")

#Check if the environment is production
IS_PRODUCTION = os.getenv("ENV") == "production"

#Session middleware for user sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    same_site = "lax" if not IS_PRODUCTION else "none",
    https_only=IS_PRODUCTION,
    max_age=3600,  
)

#Pydantic model for saving playlists payload
class SaveRequest(BaseModel):
    name: str
    description: str
    uris: List[str]

#Endpoint to get a playlist based on user's mood
@app.get("/api/playlist")
async def get_playlist(mood: str, user=Depends(get_current_user)):
    #Generates a playlist based on the user's mood. if the user is not authenticated, it raises an HTTPException.
    
    playlist = await search_playlist(mood)
    if not playlist: #No playlist found for the provided mood
        raise HTTPException(status_code=404, detail="No playlist found for this mood")
    return {"playlist": playlist}

#Endpoint to save the generated playlist to the user's Spotify account
@app.post("/api/playlist/save")
async def save_playlist( request: Request, user=Depends(get_current_user), payload: SaveRequest = Body(...)):
    #Saves the generated playlist to the user's Spotify account. Reads the access token from the session, and if not found, raises an HTTPException.
    
    access_token = request.session.get('access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail="User not authenticated")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    #Create a new playlist with the provided name and description
    #If the playlist creation fails, it raises an HTTPException with the error message.
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
    
    #Check if the playlist was created successfully
    playlist_id = created['id']
    if not playlist_id:
        raise HTTPException(status_code=500, detail="Failed to create playlist")

    #Add the tracks to the created playlist
    add_tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(add_tracks_url, headers=headers, json={"uris": payload.uris})
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,detail=f"Failed to add tracks to playlist: {e.response.text}")

    return {"url": f"https://open.spotify.com/playlist/{playlist_id}"}

#Endpoint to login with Spotify
@app.get("/auth/login")
async def login(request: Request):
    #Redirects the user to the Spotify login page.

    #Clears the session to ensure a fresh login, then redirects to Spotify's authorization URL.
    request.session.clear() 
   
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    return await oauth.spotify.authorize_redirect(request, redirect_uri=redirect_uri)

#Endpoint to handle the Spotify OAuth callback
@app.get("/auth/callback")
async def callback(request: Request):
    #Handles the Spotify OAuth callback and retrieves the access token. Token is stored in the session, and the user information is fetched from Spotify API.

    token = await oauth.spotify.authorize_access_token(request) 
    access_token = token.get('access_token')

    if not access_token:
        raise HTTPException(status_code=502, detail="Invalid access token")
    
    #persist the access token in the session
    request.session['access_token'] = access_token

    #Fetch user information from Spotify API
    user = await oauth.spotify.get('https://api.spotify.com/v1/me', token=token)

    try:
        user.raise_for_status()
    except httpx.HTTPStatusError as e:
        request.session.clear()
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch user information")
    
    #Parse the user information and store it in the session
    try:
        user_data = user.json()
    except ValueError:
        request.session.clear()
        raise HTTPException(status_code=502, detail="Failed to parse user information")
    
    #Store user information in the session
    request.session["user"] = user_data
    
    return RedirectResponse(f"/#access_token={access_token}")

#Logout endpoint to clear the session
@app.post("/auth/logout")
async def logout(request: Request):
    #Logs the user out by clearing the session.
    
    request.session.clear()
    return JSONResponse({"detail": "Logged out"})

#Static files middleware to serve the React frontend
static_directory = os.path.join(os.path.dirname(__file__), "../frontend/build")
app.mount("/", StaticFiles(directory=static_directory, html=True), name="static")