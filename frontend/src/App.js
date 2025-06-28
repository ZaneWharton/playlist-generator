import React from 'react';
import { fetchPlaylist } from './components/api.js';
import TrackList from './components/TrackList';
import LoginButton from './components/LoginButton';
import './index.css';

export default function App() {
  const [accessToken, setAccessToken] = React.useState(null);
  const [mood, setMood] = React.useState('happy');
  const [tracks, setTracks] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    const token = params.get('access_token');
    console.log(token)
    if (token) {
      setAccessToken(token);
      window.history.replaceState(null, '', window.location.pathname);
    }
  }, []);

  const handleFetch = async () => {
    setLoading(true);
    setError(null);
    try {
      const playlist = await fetchPlaylist(mood);
      setTracks(playlist || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!accessToken) {
    return (
      <div className="absolute inset-0 -z-10 h-full w-full bg-gradient-to-tr from-black via-green-800 to-black">
        <div className="flex items-center justify-center min-h-screen">
          <div className="bg-gray-800 bg-opacity-50 p-8 rounded-xl shadow-xl text-center">
            <h2 className="text-2xl font-bold text-white mb-4">Welcome to Spotify Mood Playlist</h2>
            <p className="text-gray-300 mb-6">Log in with your Spotify account to get started</p>
            <LoginButton />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="absolute inset-0 -z-10 h-full w-full bg-gradient-to-tr from-black via-green-800 to-black">
      <header className="flex justify-center items-center my-8">
        <h1 className="text-3xl font-extrabold text-green-600">Spotify Mood Playlist</h1>
      </header>

      

        <section className="flex flex-wrap justify-center gap-4 mb-6">
          <label htmlFor="mood" className="font-medium text-gray-300">Mood:</label>
          <select id="mood" value={mood} onChange={(e) => setMood(e.target.value)} className="px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-green-400">
            {['happy', 'sad', 'energetic', 'chill', 'romantic', 'motivational', 'nostalgic', 'angry', 'relaxed', 'focused'].map(m => (
              <option key={m} value={m}>{m}</option>
            ))};
          </select>
          <button onClick={handleFetch} disabled={loading} className="px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600 disabled:bg-gray-300">
            {loading ? <div className="w-5 h-5  border-2 border-t-white border-gray-200 rounded-full animate-spin mx-auto" /> : 'Get Playlist'}
          </button>
        </section>
  
      {error && <div className="text-red-600 mb-4">{error}</div>}

      {tracks.length > 0 ? <TrackList tracks={tracks}/> : <div className="flex items-center justify-center h-80"><p className="text-3xl font-bold text-green-600">Select a mood and click "Get Playlist" to start!</p></div>}
    </div>
  );
}
