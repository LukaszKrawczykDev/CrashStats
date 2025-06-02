// src/features/charts/TimeOfDayChart.jsx
import { useEffect, useState } from "react";
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

const COLLISION_TYPES = [
    "1-Car", "2-Car", "Pedestrian", "Moped/Motorcycle", "Bus", "Cyclist", "3+ Cars",
];

export default function TimeOfDayChart() {
    const [data, setData] = useState([]);
    const [types, setTypes] = useState([]);
    const [selectedTypes, setSelectedTypes] = useState(new Set(COLLISION_TYPES));
    const [showFilters, setShowFilters] = useState(false);

    useEffect(() => {
        fetchChartData();
    }, [selectedTypes]);

    async function fetchChartData() {
        try {
            const res = await fetch("/stats/time-of-day-chart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    collision_types: Array.from(selectedTypes),
                }),
            });
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            const json = await res.json();
            setData(json.data);
            setTypes(json.types);
        } catch (e) {
            console.error("Error loading chart data:", e);
        }
    }

    const toggleType = (type) => {
        const updated = new Set(selectedTypes);
        if (updated.has(type)) updated.delete(type);
        else updated.add(type);
        setSelectedTypes(updated);
    };

    return (
        <div className="w-full h-64 md:h-[400px]">
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold">Pora dnia a typ wypadku</h3>
                <button
                    className="text-sm underline"
                    onClick={() => setShowFilters((prev) => !prev)}
                >
                    {showFilters ? "Ukryj filtry" : "Pokaż filtry"}
                </button>
            </div>

            {showFilters && (
                <div className="flex flex-wrap gap-4 mb-4">
                    {COLLISION_TYPES.map((type) => (
                        <label key={type} className="flex items-center gap-1 text-sm">
                            <input
                                type="checkbox"
                                checked={selectedTypes.has(type)}
                                onChange={() => toggleType(type)}
                            />
                            {type}
                        </label>
                    ))}
                </div>
            )}

            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {types.map((type) => (
                        <Bar
                            key={type}
                            dataKey={type}
                            stackId="a"
                            fill="#3b82f6"
                        />
                    ))}
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}