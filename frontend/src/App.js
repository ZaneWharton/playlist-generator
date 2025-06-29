import { useEffect, useState } from 'react';
import { fetchPlaylist } from './components/api.js';
import TrackList from './components/TrackList';
import LoginButton from './components/LoginButton';
import LogoutButton from './components/LogoutButton.jsx';
import './index.css';

export default function App() {
  const [accessToken, setAccessToken] = useState(null);
  const [mood, setMood] = useState('happy');
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastMood, setLastMood] = useState('None');
  const [excludeExplicit, setExcludeExplicit] = useState(false); 

  const [playlistName, setPlaylistName] = useState('');
  const [playlistDescription, setPlaylistDescription] = useState('');
  const [playlistUrl, setPlaylistUrl] = useState(null);

  useEffect(() => {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    const token = params.get('access_token');
    if (token) {
      setAccessToken(token);
      window.history.replaceState(null, '', window.location.pathname);
    }
  }, []);

  const handleFetch = async () => {
    setPlaylistUrl(null);
    setPlaylistName('');
    setPlaylistDescription('');
    
    setLoading(true);
    setError(null);
    try {
      const playlist = await fetchPlaylist(mood);
      const filteredTracks = excludeExplicit ? playlist.filter(track => !track.explicit) : playlist;
      setTracks(filteredTracks || []);
      setLastMood(mood);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!playlistName.trim()) {return alert('Please enter a playlist name');}
    const uris = tracks.map(track => track.uri);
    try {
      const response = await fetch(`/api/playlist/save`, {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: playlistName, description: playlistDescription, uris }),
      });
      if (!response.ok) {
        throw new Error('Failed to save playlist');
      }
      const {url} = await response.json();
      setPlaylistUrl(url);

    } catch (err) {
      console.error('Error saving playlist:', err);
      alert('Failed to save playlist. Please try again.');
    }
  };

  const handleLogout = () => {
    setAccessToken(null);
    setTracks([]);
    setMood('happy');
    setPlaylistName('');
    setPlaylistDescription('');
    setPlaylistUrl(null);
  };

  if (!accessToken) {
    return (
      <div className="absolute h-full w-full bg-gradient-to-tr from-black via-green-800 to-black px-4 py-8">
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
    <div className="absolute h-full w-full bg-gradient-to-tr from-black via-green-800 to-black px-4 py-8">
      <header className="flex justify-center my-8">
        <h1 className="text-3xl font-extrabold text-green-600">Spotify Mood Playlist</h1>
      </header>

      

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-center gap-2 mb-6">
        <label htmlFor="mood" className="font-medium text-sm text-gray-300">What mood are you in?</label>
        <select id="mood" value={mood} onChange={(e) => setMood(e.target.value)} className="px-1 py-1 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-2 hover:ring-2 ring-green-400 cursor-pointer">
          {['happy', 'sad', 'energetic', 'chill', 'romantic', 'motivational', 'nostalgic', 'angry', 'relaxed', 'focused'].map(m => (
            <option key={m} value={m}>{m}</option>
          ))};
        </select>
        <label htmlFor="excludeExplicit" className="font-medium text-sm text-gray-300">Exclude Explicit Tracks?</label>
        <input type="checkbox" id="excludeExplicit" checked={excludeExplicit} onChange={(e) => setExcludeExplicit(e.target.checked)} className="cursor-pointer" />
        <button onClick={handleFetch} disabled={loading} className="px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600 disabled:bg-gray-300">
          {loading ? <div className="w-5 h-5 border-2 border-t-white border-gray-200 rounded-full animate-spin mx-auto" /> : 'Get Playlist'}
        </button>
      </div>
  
      {error && <div className="text-red-600 mb-4">{error}</div>}
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className="text-gray-300 text-center md:text-left">
          <h2 className="text-2xl font-bold mb-2">Current Playlist</h2>
          <p className="capitalize text-gray-300">Mood: <span className="text-green-400">{lastMood}</span></p>
          <p className="text-gray-300">Tracks: <span className="text-green-400">{tracks.length}</span></p>
        </div>

        <div className="flex justify-center">
          {tracks.length > 0 ? <TrackList tracks={tracks}/> : <p className="text-3xl font-bold text-green-600 my-20">No tracks yet!</p>}
        </div>

        <div className="text-center">
          <input type="text" placeholder="Playlist Name" value={playlistName} onChange={(e) => setPlaylistName(e.target.value)} className="w-4/5 mx-4 mb-2 p-2 rounded bg-gray-700 text-white" />
          <textarea placeholder="Playlist Description" value={playlistDescription} onChange={(e) => setPlaylistDescription(e.target.value)} className="w-4/5 mx-4 mb-2 p-2 rounded bg-gray-700 text-white"></textarea>
          <button onClick={handleSave} className="w-4/5 mx-4 px-4 py-2 bg-green-500 rounded hover:bg-green-600">Save playlist to Spotify</button>
          {playlistUrl && (
            <p className="text-green-400">Playlist saved successfully! <a href={playlistUrl} target="_blank" rel="noopener noreferrer" className="underline">Open Playlist</a></p>
          )}
          <p className="text-gray-300 mt-4">Powered by Spotify API</p>
          <LogoutButton onLogout={handleLogout} />
        </div>
      </div>
    </div>
  );
}
