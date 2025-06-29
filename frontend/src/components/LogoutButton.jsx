export default function LogoutButton({ onLogout }) {
    // Send a request to the FastAPI logout endpoint
    
    const handleLogout = async () => {
        const BASE_URL = process.env.REACT_APP_API_URL
        try {
            await fetch(`${BASE_URL}/auth/logout`, {
                method: 'POST',
                credentials: 'include', 
            });
            onLogout();
        } catch (error) {
            console.error('Logout failed:', error);
            }
        };

        return (
            <button onClick={handleLogout} className="px-4 py-2 text-gray-400 font-semibold text-sm hover:underline">
                Log Out
            </button>
        );
}