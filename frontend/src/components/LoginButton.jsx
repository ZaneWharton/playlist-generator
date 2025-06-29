export default function LoginButton() {
  const handleLogin = () => {
    // Redirect to FastAPI OAuth endpoint
    window.location.href = `http://127.0.0.1:8000/auth/login`;
  };

  return (
    <button onClick={handleLogin} className="px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600">
      Log In with Spotify
    </button>
  );
}