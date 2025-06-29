import os
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi import Request

BASE = os.path.dirname(os.path.abspath(__file__))
DOTENV_FILE = os.path.join(BASE, ".env")

if os.path.exists(DOTENV_FILE):
    load_dotenv(dotenv_path=DOTENV_FILE)

oauth = OAuth()
oauth.register(
    name='spotify',
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize',
    client_kwargs={'scope': ('user-read-private user-read-email playlist-modify-private playlist-modify-public')},
)

async def get_current_user(request: Request):
    # Retrieves the current user from the session.

    user = request.session.get('user')
    print("session: ", request.session)
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user

