# Spotify Mood Playlist Generator

A full stack app that generates and saves mood-based Spotify playlists. 

## Features

- **Spotify OAuth** - Users log in with their Spotify account.
- **Mood-Based Playlists** - Users select a mood, and a playlist is generated by selecting random tracks from genres associated with the selected mood.
- **Explicit-Track Filter** - Users have the option to exclude explicit songs from their playlist.
- **Save to Spotify** - Users and name their playlist, provide a description, and save the playlist to their Spotify account.

## Tech Stack

- **Backend:** FastAPI, Authlib, HTTPX, Pydantic
- **Frontend:** React, Tailwind CSS
- **Testing:** Pytest, Pytest-Asyncio, HTTPX, React Testing Library

## Setup

# Environment Variables

Create a .env file in the backend directory with the following variables:

```dotenv
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SESSION_SECRET_KEY=your_session_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
FRONTEND_URL=http://127.0.0.1:8000
ENV=development
```

# App Setup
Prepare the backend:
```
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Prepare the frontend:
```
cd frontend
npm install
npm run build
```

The app is designed to run the frontend and backend on the same domain, npm run build will prepare a static file for the backend. Run the app from the root directory:
```
uvicorn backend.main:app --reload
```

## Running Tests

# Backend
```
cd backend
pytest
```

# Frontend
```
cd frontend
npm test
```

## Live Demo
This app is deployed to Render. Visit https://mood-playlist-generator-bix9.onrender.com

