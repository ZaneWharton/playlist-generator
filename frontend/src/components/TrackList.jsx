//Render a list of Spotify tracks with navigation buttons

import { useState } from 'react';

export default function TrackList({ tracks }) {
    //State to manage the current index of the track being displayed
    const [index, setIndex] = useState(0);

    //If no tracks are provided, display a message
    const validTracks = tracks.filter(track => track.id && track.uri);
    if (!validTracks.length) return <p className="text-3xl font-bold text-green-600 mt-20">No valid tracks available!</p>;

    //Calculate the total number of valid tracks and get the current track based on the index
    //If there are no valid tracks, return null to avoid rendering errors
    const total = validTracks.length;
    const track = validTracks[index];
    if (!total) return null;

    //Render the track list with navigation buttons
    return (
        <div className="flex items-center justify-center gap-4 w-full px-4">
            <button
                onClick={() => setIndex((index - 1 + total) % total)}
                className="cursor-pointer text-green-500 text-5xl hover:text-green-600"
            >&larr;</button>
        
            <div className="bg-gray-800 bg-opacity-50 p-4 w-full sm:max-w-lg rounded-xl shadow-xl">
                <iframe src={"https://open.spotify.com/embed/track/" + track.id} className="w-full h-[80px] md:h-[365px] rounded-lg" allow="encrypted-media"></iframe>
            </div>
            
            <button
                onClick={() => setIndex((index + 1) % total)}
                className="cursor-pointer text-green-500 text-5xl hover:text-green-600"
            >&rarr;</button>
        </div>
    )
}