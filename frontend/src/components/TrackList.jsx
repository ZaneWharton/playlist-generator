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
                    className="cursor-pointer text-green-500 text-5xl hover:text-green-600"
                >&larr;</button>
            </div>

            <div className="bg-gray-800 bg-opacity-50 p-8 rounded-xl shadow-xl text-center">
                <iframe src={"https://open.spotify.com/embed/track/" + track.id} className="mt-4 w-[600px] h-[375px]" allow="encrypted-media"></iframe>
            </div>
            
            <div className="my-auto">
                <button
                    onClick={() => setIndex((index + 1) % total)}
                    className="cursor-pointer text-green-500 text-5xl hover:text-green-600"
                >&rarr;</button>
            </div>
        </div>
    )
}