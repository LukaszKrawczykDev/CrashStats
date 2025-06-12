import { useEffect, useState, useMemo } from "react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from "recharts";
import ChartModal from "./ChartModal";
import { Checkbox } from "../ui/checkbox";

const injuryColors = {
    "Fatal": "#ef4444",
    "Incapacitating": "#10b981",
    "Non-incapacitating": "#f59e0b",
    "No injury/unknown": "#3b82f6",
    "OTHER": "#6b7280",
};

const INJURY_KEYS = Object.keys(injuryColors);

export default function WeatherChart() {
    const [dimension, setDimension] = useState("category"); // albo 'road_condition'
    const [injuryFilter, setInjuryFilter] = useState(new Set(INJURY_KEYS));
    const [data, setData] = useState([]);
    const [open, setOpen] = useState(false);

    useEffect(() => {
        (async () => {
            try {
                const res = await fetch("/api/stats/weather-chart", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        dimension,
                        injury_types: Array.from(injuryFilter),
                    }),
                });
                const json = await res.json();
                setData(
                    json.map((row) => ({
                        dim: row.dim,
                        ...row,
                    }))
                );
            } catch (e) {
                console.error("Błąd fetchowania weather-chart", e);
            }
        })();
    }, [dimension, injuryFilter]);

    const toggleInjury = (k) => {
        setInjuryFilter((prev) => {
            const copy = new Set(prev);
            copy.has(k) ? copy.delete(k) : copy.add(k);
            return copy;
        });
    };

    const bars = useMemo(
        () =>
            INJURY_KEYS.filter((k) => injuryFilter.has(k) || open) // w mini-widoku pokazujemy tylko zaznaczone
                .map((k) => (
                    <Bar
                        key={k}
                        dataKey={k}
                        stackId="a"
                        fill={injuryColors[k]}
                        isAnimationActive={false}
                    />
                )),
        [injuryFilter, open]
    );

    const handleBarClick = (e) => {
        // wysyłam globalne zdarzenie; w LocationMap możesz to podsłuchać
        window.dispatchEvent(
            new CustomEvent("weather-filter", { detail: { dim: e.activeLabel, dimension } })
        );
    };

    return (
        <>
            <div
                className="w-full h-64 cursor-pointer"
                onClick={() => setOpen(true)}
            >
                <h3 className="text-lg font-semibold mb-2">
                    Wypadki a pogoda&nbsp;
                    <span className="text-sm text-gray-500">
            ({dimension === "category" ? "typ aury" : "stan nawierzchni"})
          </span>
                </h3>
                <ResponsiveContainer width="100%" height="85%">
                    <BarChart data={data} onClick={handleBarClick}>
                        <XAxis dataKey="dim" tick={{ fontSize: 11 }} />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        {bars}
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <ChartModal
                isOpen={open}
                onClose={() => setOpen(false)}
            >
                <div className="flex items-center gap-4 mb-4">
                    <label className="flex items-center gap-1">
                        <input
                            type="radio"
                            name="dim"
                            value="category"
                            checked={dimension === "category"}
                            onChange={() => setDimension("category")}
                        />
                        <span>Typ aury (weather.category)</span>
                    </label>
                    <label className="flex items-center gap-1">
                        <input
                            type="radio"
                            name="dim"
                            value="road_condition"
                            checked={dimension === "road_condition"}
                            onChange={() => setDimension("road_condition")}
                        />
                        <span>Stan nawierzchni (weather.road_condition)</span>
                    </label>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-x-6 gap-y-2 mb-6">
                    {INJURY_KEYS.map((k) => (
                        <label key={k} className="flex items-center gap-2">
                            <Checkbox
                                checked={injuryFilter.has(k)}
                                onChange={() => toggleInjury(k)}
                            />
                            <span style={{ color: injuryColors[k] }}>{k}</span>
                        </label>
                    ))}
                </div>
                <div className="w-full h-[28rem]">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={data} onClick={handleBarClick}>
                            <XAxis dataKey="dim" tick={{ fontSize: 12, angle: -30, dy: 8 }} />
                            <YAxis allowDecimals={false} />
                            <Tooltip />
                            <Legend />
                            {INJURY_KEYS.filter((k) => injuryFilter.has(k)).map((k) => (
                                <Bar
                                    key={k}
                                    dataKey={k}
                                    stackId="a"
                                    fill={injuryColors[k]}
                                    isAnimationActive={false}
                                />
                            ))}
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </ChartModal>
        </>
    );
}