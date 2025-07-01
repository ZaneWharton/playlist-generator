# Test suite for the FastAPI application

import pytest
from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from backend.main import app

#Fixture to create an ASGI client for testing
@fixture
async def client():
    # Create an ASGI transport for the FastAPI app

    transport = ASGITransport(app=app)
    ac = AsyncClient(transport=transport, base_url="http://test")
    yield ac

    #Cleanup
    await ac.aclose()

#Authentication tests
@pytest.mark.asyncio
async def test_login_redirect(client):
    #Hitting /auth/login should redirect the user to Spotify's authorize URL.
    
    response = await client.get("/auth/login")
    assert response.status_code in (302, 307)
    assert "accounts.spotify.com/authorize" in response.headers["location"]

@pytest.mark.asyncio
async def test_logout_success(client):
    #Hitting /auth/logout should redirect the user to the home page.
    
    response = await client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"detail": "Logged out"}

@pytest.mark.asyncio
async def test_playlist_requires_auth(client):
    #Unauthenticated requests to /api/playlist should be rejected with 401.
    
    response = await client.get("/api/playlist?mood=happy")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_save_requires_auth(client):
    #Unauthenticated requests to /api/save_playlist should be rejected with 401.
    
    response = await client.post("/api/playlist/save", json={"mood": "happy", "tracks": []})
    assert response.status_code == 401
