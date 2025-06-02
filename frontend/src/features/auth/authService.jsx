const API = import.meta.env.VITE_API_URL;

export async function loginUser({ username, password }) {
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);

    const response = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body,
    });

    if (!response.ok) {
        throw new Error("Błąd logowania");
    }

    return await response.json();
}

export async function registerUser({ username, email, password }) {
    const response = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
    });

    if (!response.ok) {
        throw new Error("Błąd rejestracji");
    }

    return await response.json();
}