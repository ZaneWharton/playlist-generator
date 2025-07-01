//Fetch playlist based on mood from the backend API

export async function fetchPlaylist(mood) {
    //Build the URL for the API request
    const url = `/api/playlist?mood=${encodeURIComponent(mood)}`;

    //Make the GET request to the backend API
    const response = await fetch(url, {
        method: 'GET',
        credentials: 'include', 
    });

    //Check if the response is ok, if not throw an error
    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${response.status}`);
    }
    const data = await response.json();
    return data.playlist.tracks.items;
}