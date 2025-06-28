#Run the server: uvicorn main:app --reload

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from auth import oauth, get_current_user
from spotify import search_playlist
import os
from dotenv import load_dotenv

app = FastAPI(title="Mood Playlist Generator")
load_dotenv()

# Session middleware for user sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
    same_site = "lax",
    https_only=False,
)

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Adjust this to your frontend URL in production
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,

)

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
    print(access_token)
    request.session['user'] = user.json()
    return RedirectResponse(f"http://127.0.0.1:3000/#access_token={access_token}")

@app.get("/api/playlist")
async def get_playlist(mood: str, user=Depends(get_current_user)):
    #Generates a playlist based on the user's mood.
    
    playlist = await search_playlist(mood)
    if not playlist:
        raise HTTPException(status_code=404, detail="No playlist found for this mood")
    return {"playlist": playlist}

    
    


