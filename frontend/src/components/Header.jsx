// src/components/Header.jsx
import { Link } from "react-router-dom";
import { useState } from "react";
import AuthModal from "./AuthModal";
import { useAuth } from "../features/auth/authContext.jsx";

export default function Header() {
    const [showModal, setShowModal] = useState(false);
    const { token, role, logout } = useAuth();

    return (
        <>
            <header className="sticky top-0 z-50 bg-gray-800 text-white p-4 flex justify-between items-center shadow">
                <h1 className="text-xl font-bold">🚗 CrashStats</h1>
                <div>
                    {token && (
                        <>
                            <Link to="/export" className="bg-blue-500 px-4 py-2 rounded mr-2">
                                Eksportuj dane
                            </Link>
                        </>
                    )}
                    {!token ? (
                        <button onClick={() => setShowModal(true)} className="bg-blue-600 px-4 py-2 rounded">
                            Zaloguj się
                        </button>
                    ) : (
                        <button onClick={logout} className="bg-red-500 px-4 py-2 rounded">
                            Wyloguj
                        </button>
                    )}
                </div>
            </header>
            <AuthModal isOpen={showModal} onClose={() => setShowModal(false)} />
        </>
    );
}