// src/components/charts/AccidentsByMonth.jsx
import { useEffect, useState } from "react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const ROAD_CONDITIONS = ["snowy", "icy", "wet", "dry"];
const COLORS = {
    snowy: "#60a5fa",
    icy: "#7dd3fc",
    wet: "#38bdf8",
    dry: "#0ea5e9"
};

export default function AccidentsByMonth({ filters, expanded = false }) {
    const [chartData, setChartData] = useState([]);
    const [activeConditions, setActiveConditions] = useState(ROAD_CONDITIONS);
    const [stats, setStats] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch("/api/stats/accidents-by-month", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(filters)
                });

                if (!res.ok) throw new Error("Błąd pobierania danych");
                const raw = await res.json();

                let newStats = {};
                const formatted = raw.map(({ year, month, breakdown }) => {
                    let total = 0;
                    for (const cond of ROAD_CONDITIONS) {
                        total += breakdown[cond] || 0;
                        newStats[cond] = (newStats[cond] || 0) + (breakdown[cond] || 0);
                    }

                    return {
                        label: `${month.toString().padStart(2, "0")}.${year}`,
                        ...breakdown,
                        total
                    };
                });

                setChartData(formatted);
                setStats(newStats);
            } catch (err) {
                console.error("Błąd podczas fetchowania danych:", err);
                setChartData([]);
                setStats({});
            }
        };

        fetchData();
    }, [filters]);

    const toggleCondition = (cond) => {
        setActiveConditions((prev) =>
            prev.includes(cond) ? prev.filter((c) => c !== cond) : [...prev, cond]
        );
    };

    return (
        <div className="w-full">
            <div className="w-full h-72">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                        <XAxis dataKey="label" />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        {ROAD_CONDITIONS.map((cond) =>
                            activeConditions.includes(cond) ? (
                                <Bar key={cond} dataKey={cond} stackId="a" fill={COLORS[cond]} />
                            ) : null
                        )}
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {expanded && (
                <div className="mt-4 flex flex-col md:flex-row gap-6">
                    {/* FILTRY */}
                    <div>
                        <h4 className="font-semibold mb-2">Filtruj wg pogody</h4>
                        {ROAD_CONDITIONS.map((cond) => (
                            <label key={cond} className="block text-sm">
                                <input
                                    type="checkbox"
                                    checked={activeConditions.includes(cond)}
                                    onChange={() => toggleCondition(cond)}
                                    className="mr-2"
                                />
                                {cond}
                            </label>
                        ))}
                    </div>

                    {/* STATYSTYKI */}
                    <div>
                        <h4 className="font-semibold mb-2">Statystyki</h4>
                        <ul className="text-sm space-y-1">
                            {Object.entries(stats).map(([cond, value]) => (
                                <li key={cond}>
                                    {cond}: <span className="font-medium">{value}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
}