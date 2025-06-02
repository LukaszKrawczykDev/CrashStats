import React, { useState } from "react";
import { useAuth } from "../features/auth/authContext";
import { loginUser, registerUser } from "../features/auth/authService";

const AuthModal = ({ isOpen, onClose }) => {
    const { login } = useAuth();
    const [isLoginMode, setIsLoginMode] = useState(true);

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const result = isLoginMode
                ? await loginUser({ username, password })
                : await registerUser({ username, email, password });

            login(result.access_token, result.role);
            onClose();
        } catch (err) {
            setError(err.response?.data?.detail || "Błąd podczas logowania/rejestracji");
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-sm">
                <h2 className="text-xl font-semibold mb-4">
                    {isLoginMode ? "Logowanie" : "Rejestracja"}
                </h2>
                <form onSubmit={handleSubmit} className="space-y-3">
                    {error && <p className="text-red-600">{error}</p>}

                    <input
                        type="text"
                        placeholder="Nazwa użytkownika"
                        className="border p-2 w-full"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />

                    {!isLoginMode && (
                        <input
                            type="email"
                            placeholder="Email"
                            className="border p-2 w-full"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    )}

                    <input
                        type="password"
                        placeholder="Hasło"
                        className="border p-2 w-full"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />

                    <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded w-full">
                        {isLoginMode ? "Zaloguj się" : "Zarejestruj się"}
                    </button>
                </form>

                <div className="mt-4 text-sm text-center">
                    {isLoginMode ? (
                        <>
                            Nie masz konta?{" "}
                            <button className="text-blue-600" onClick={() => setIsLoginMode(false)}>
                                Zarejestruj się
                            </button>
                        </>
                    ) : (
                        <>
                            Masz już konto?{" "}
                            <button className="text-blue-600" onClick={() => setIsLoginMode(true)}>
                                Zaloguj się
                            </button>
                        </>
                    )}
                </div>

                <button onClick={onClose} className="mt-4 text-gray-600 text-sm w-full">
                    Zamknij
                </button>
            </div>
        </div>
    );
};

export default AuthModal;