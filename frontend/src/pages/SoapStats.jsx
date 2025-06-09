import { useEffect, useState } from "react";

export default function SoapStats() {
    const [stats, setStats] = useState(null);
    const [error, setError] = useState(null);

    // odczyt URL z .env
    const API_URL = import.meta.env.VITE_API_URLL;

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await fetch(`${API_URL}/api/soap/stats`, {
                    mode: "cors"
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                if (data.error) throw new Error(data.error);
                setStats(data);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchStats();
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">📊 Statystyki (SOAP)</h1>
            {error && <p className="text-red-600">❌ {error}</p>}
            {!stats && !error && <p className="text-gray-600">Ładowanie…</p>}
            {stats && (
                <ul className="list-disc list-inside space-y-1">
                    <li>Liczba wypadków: {stats.accidents_total}</li>
                    <li>Unikalne lokalizacje: {stats.unique_locations}</li>
                    <li>Unikalne daty: {stats.unique_dates}</li>
                    <li>Najczęstszy typ kolizji: {stats.most_common_type}</li>
                    <li>Najczęstszy czynnik: {stats.most_common_factor}</li>
                </ul>
            )}
        </div>
    );
}