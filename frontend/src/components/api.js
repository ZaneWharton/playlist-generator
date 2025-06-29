export async function fetchPlaylist(mood) {
    const url = `http://127.0.0.1:8000/api/playlist?mood=${encodeURIComponent(mood)}`;
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