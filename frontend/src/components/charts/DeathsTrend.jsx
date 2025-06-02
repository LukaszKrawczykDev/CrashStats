// src/components/charts/DeathsTrend.jsx
import { useEffect, useState } from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Legend
} from "recharts";

const COLORS = {
    "Fatal": "#f87171",
    "Non-incapacitating": "#60a5fa",
    "Incapacitating": "#a78bfa",
    "No injury/unknown": "#34d399",
    "Other": "#fbbf24"
};

const INJURY_TYPES = ["Fatal", "Non-incapacitating", "Incapacitating", "No injury/unknown", "Other"];

export default function DeathsTrend({ filters, isFullscreen = false }) {
    const [data, setData] = useState([]);
    const [activeLines, setActiveLines] = useState(() => new Set(INJURY_TYPES));

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch("/api/stats/deaths-trend", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(filters)
                });

                if (!res.ok) throw new Error("Błąd pobierania danych");
                const raw = await res.json();
                setData(raw);
            } catch (err) {
                console.error("Błąd podczas pobierania danych:", err);
                setData([]);
            }
        };

        fetchData();
    }, [filters]);

    const toggleLine = (type) => {
        setActiveLines((prev) => {
            const newSet = new Set(prev);
            newSet.has(type) ? newSet.delete(type) : newSet.add(type);
            return newSet;
        });
    };

    return (
        <div className="w-full">
            <div className="h-64 md:h-96">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="label" angle={-45} textAnchor="end" height={60} />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        <Legend />
                        {INJURY_TYPES.map((type) =>
                            activeLines.has(type) ? (
                                <Line
                                    key={type}
                                    type="monotone"
                                    dataKey={type}
                                    stroke={COLORS[type]}
                                    strokeWidth={2}
                                    dot={false}
                                />
                            ) : null
                        )}
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {isFullscreen && (
                <div className="mt-4">
                    <h4 className="text-md font-semibold mb-2">Typy obrażeń</h4>
                    <div className="flex flex-wrap gap-4">
                        {INJURY_TYPES.map((type) => (
                            <label key={type} className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    checked={activeLines.has(type)}
                                    onChange={() => toggleLine(type)}
                                />
                                <span style={{ color: COLORS[type] }}>{type}</span>
                            </label>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
//TODO Dodać checkbox