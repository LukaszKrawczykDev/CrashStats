// src/features/charts/WeatherChart.jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
    { weather: "Słonecznie", count: 220 },
    { weather: "Deszcz", count: 130 },
    { weather: "Śnieg", count: 60 },
    { weather: "Mgła", count: 40 },
];

export default function WeatherChart() {
    return (
        <div className="w-full h-64">
            <h3 className="text-lg font-semibold mb-2">Wypadki a pogoda</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <XAxis dataKey="weather" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#34d399" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}