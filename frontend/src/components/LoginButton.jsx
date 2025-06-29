export default function LoginButton() {
  const handleLogin = () => {
    // Redirect to FastAPI OAuth endpoint
    const BASE_URL = process.env.REACT_APP_API_URL
    window.location.href = `${BASE_URL}/auth/login`;
  };

  return (
    <button onClick={handleLogin} className="px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600">
      Log In with Spotify
    </button>
  );
}