//Handle user login by redirecting to the FastAPI OAuth endpoint

export default function LoginButton() {
  const handleLogin = () => {
    // Redirect to FastAPI OAuth endpoint
    window.location.href = `/auth/login`;
  };

  return (
    <button onClick={handleLogin} className="px-4 py-2 bg-green-500 text-white font-semibold rounded hover:bg-green-600">
      Log In with Spotify
    </button>
  );
}