// src/pages/ImportPage.jsx
import React, { useState } from "react";
import { useAuth } from "../features/auth/authContext";

const API = import.meta.env.VITE_API_URL; // np. "http://localhost:8000"

export default function ImportPage() {
    const { token } = useAuth();
    const [file, setFile] = useState(null);
    const [results, setResults] = useState([]);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setResults([]);
    };

    const handleImport = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        try {
            const resp = await fetch(`${API}/api/import`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                body: formData,
            });

            if (!resp.ok) {
                const err = await resp.json();
                setResults([{ row: 0, status: "error", error: err.detail || resp.statusText }]);
                return;
            }

            const data = await resp.json();
            setResults(data);
        } catch (e) {
            setResults([{ row: 0, status: "error", error: e.message }]);
        }
    };

    return (
        <div className="max-w-xl mx-auto p-6">
            <h2 className="text-2xl font-semibold mb-4">Import danych</h2>

            <div className="flex items-center space-x-4 mb-6">
                <input
                    type="file"
                    accept=".xml,.json,.yml,.yaml"
                    onChange={handleFileChange}
                />
                <button
                    onClick={handleImport}
                    disabled={!file}
                    className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
                >
                    Importuj
                </button>
            </div>

            <div className="space-y-2">
                {results.map((r) => (
                    <p
                        key={r.row}
                        className={r.status === "success" ? "text-green-700" : "text-red-700"}
                    >
                        Wiersz {r.row}:{" "}
                        {r.status === "success"
                            ? "✅ wgrany"
                            : `❌ odrzucony (${r.error})`}
                    </p>
                ))}
            </div>
        </div>
    );
}