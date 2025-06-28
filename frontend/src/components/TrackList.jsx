import {useState} from 'react';

export default function TrackList({ tracks }) {
    const [index, setIndex] = useState(0);
    const total = tracks.length;
    const track = tracks[index];
    if (!total) return null;

    return (
        <div className="relative flex justify-center">
            <div className="my-auto">
                <button
                    onClick={() => setIndex((index - 1 + total) % total)}
                    className="cursor-pointer text-green-500 text-5xl"
                >&larr;</button>
            </div>

            <div className="bg-gray-800 bg-opacity-50 p-8 rounded-xl shadow-xl text-center">
                <img src={track.album.images[0].url} className="h-60 w-60"/>
                <h3 className="font-semibold text-lg text-gray-300 w-60">{track.name}</h3>
                <p className="text-sm text-gray-400 w-60">{track.artists.map(a => a.name).join(', ')}</p>
                <p><a href={track.external_urls.spotify} target="_blank" rel="noopener noreferrer" className="text-green-500 hover:underline">Listen on Spotify</a></p>
            </div>
            
            <div className="my-auto">
                <button
                    onClick={() => setIndex((index + 1) % total)}
                    className="cursor-pointer text-green-500 text-5xl"
                >&rarr;</button>
            </div>
        </div>
    )
}