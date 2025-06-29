export default function LogoutButton({ onLogout }) {
    // Send a request to the FastAPI logout endpoint
    
    const handleLogout = async () => {
        try {
            await fetch(`/auth/logout`, {
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