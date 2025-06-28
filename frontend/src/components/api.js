export async function fetchPlaylist(mood) {
    const url = `/api/playlist?mood=${encodeURIComponent(mood)}`;
    const resp = await fetch(url, {
        method: 'GET',
        credentials: 'include',   // ← send & receive cookies
    });
    if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${resp.status}`);
    }
    const data = await resp.json();
    console.log('Fetched playlist:', data.playlist.tracks.items);
    return data.playlist.tracks.items;
}