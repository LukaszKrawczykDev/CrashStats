import { useEffect, useState } from "react";
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

const COLLISION_TYPES = [
    "1-Car", "2-Car", "Pedestrian", "Moped/Motorcycle", "Bus", "Cyclist", "3+ Cars"
];
const COLORS = ["#60a5fa", "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#14b8a6"];

export default function UserTypeWeatherChart() {
    const [data, setData] = useState([]);
    const [types, setTypes] = useState(COLLISION_TYPES);
    const [selectedTypes, setSelectedTypes] = useState(new Set(COLLISION_TYPES));
    const [showFilters, setShowFilters] = useState(false);

    useEffect(() => {
        fetch("/api/stats/user-weather-chart", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ collision_types: Array.from(selectedTypes) })
        })
            .then((res) => {
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                return res.json();
            })
            .then((json) => {
                setData(json.data);
                setTypes(json.types);
            })
            .catch((err) => {
                console.error("Błąd ładowania danych wykresu:", err);
            });
    }, [selectedTypes]);

    const toggleType = (type) => {
        const copy = new Set(selectedTypes);
        copy.has(type) ? copy.delete(type) : copy.add(type);
        setSelectedTypes(copy);
    };

    return (
        <div className="w-full h-64 md:h-[400px]">
            <div className="flex items-center justify-between mb-2">
                <button
                    className="text-sm underline"
                    onClick={() => setShowFilters((prev) => !prev)}
                >
                    {showFilters ? "Ukryj filtry" : "Pokaż filtry"}
                </button>
            </div>

            {showFilters && (
                <div className="flex flex-wrap gap-4 mb-4">
                    {COLLISION_TYPES.map((ct) => (
                        <label key={ct} className="flex items-center gap-1 text-sm">
                            <input
                                type="checkbox"
                                checked={selectedTypes.has(ct)}
                                onChange={() => toggleType(ct)}
                            />
                            {ct}
                        </label>
                    ))}
                </div>
            )}

            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <XAxis dataKey="label" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Legend />
                    {types.map((ct, i) => (
                        <Bar key={ct} dataKey={ct} stackId="a" fill={COLORS[i % COLORS.length]} />
                    ))}
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}