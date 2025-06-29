export async function fetchPlaylist(mood) {
    const BASE_URL = process.env.REACT_APP_API_URL
    const url = `${BASE_URL}/api/playlist?mood=${encodeURIComponent(mood)}`;
    const resp = await fetch(url, {
        method: 'GET',
        credentials: 'include', 
    });
    if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${resp.status}`);
    }
    const data = await resp.json();
    return data.playlist.tracks.items;
}