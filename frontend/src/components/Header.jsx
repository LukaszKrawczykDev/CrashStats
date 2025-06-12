import { Link } from "react-router-dom";
import { useState } from "react";
import AuthModal from "./AuthModal";
import { useAuth } from "../features/auth/authContext.jsx";

export default function Header() {
    const [showModal, setShowModal] = useState(false);
    const { token, role, logout } = useAuth();
    const [showImporter, setShowImporter] = useState(false);

    return (
        <>
            <header className="sticky top-0 z-50 bg-gray-800 text-white p-4 flex justify-between items-center shadow">
                <Link to="/" className="text-xl font-bold">
                    🚗 CrashStats
                </Link>
                <div className="space-x-2">
                    <Link to="/soap-stats" className="bg-purple-600 px-4 py-2 rounded ml-2">
                        Statystyki - SOAP
                    </Link>
                    {!token ? (
                        <button onClick={() => setShowModal(true)} className="bg-blue-600 px-4 py-2 rounded">
                            Zaloguj się
                        </button>
                    ) : (
                        <>
                            <Link to="/export" className="bg-green-500 px-4 py-2 rounded">
                                Eksportuj dane
                            </Link>
                            {role === "admin" && (
                                <Link to="/import" className="bg-yellow-500 px-4 py-2 rounded">
                                    Importuj dane
                                </Link>
                            )}
                            <button onClick={logout} className="bg-red-500 px-4 py-2 rounded">
                                Wyloguj
                            </button>
                        </>
                    )}
                </div>
            </header>
            <AuthModal isOpen={showModal} onClose={() => setShowModal(false)} />
        </>
    );
}