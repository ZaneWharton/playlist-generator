import {useState} from 'react';

export default function TrackList({ tracks }) {
    const [index, setIndex] = useState(0);

    const validTracks = tracks.filter(track => track.id && track.uri);
    if (!validTracks.length) return <p className="text-3xl font-bold text-green-600 mt-20">No valid tracks available!</p>;

    const total = validTracks.length;
    const track = validTracks[index];
    if (!total) return null;

    return (
        <div className="flex items-center justify-center gap-4 w-full overflow-x-auto px-4">
            <div className="my-auto">
                <button
                    onClick={() => setIndex((index - 1 + total) % total)}
                    className="cursor-pointer text-green-500 text-5xl hover:text-green-600 flex-shrink-0"
                >&larr;</button>
            </div>

            <div className="flex-shrink-0 w-4/5 sm:w-2/3 md:w-1/2 lg:w-1/3 bg-gray-800 bg-opacity-50 p-4 rounded-xl shadow-xl">
                <div className="relative">
                    <iframe src={"https://open.spotify.com/embed/track/" + track.id} className="absolute inset-0 w-full h-full rounded-lg" allow="encrypted-media"></iframe>
                </div>
            </div>
            
            <div className="my-auto">
                <button
                    onClick={() => setIndex((index + 1) % total)}
                    className="cursor-pointer text-green-500 text-5xl hover:text-green-600 flex-shrink-0"
                >&rarr;</button>
            </div>
        </div>
    )
}