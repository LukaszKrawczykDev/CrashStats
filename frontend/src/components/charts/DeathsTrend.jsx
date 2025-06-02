// src/features/charts/DeathsTrend.jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
    { year: 2018, deaths: 320 },
    { year: 2019, deaths: 295 },
    { year: 2020, deaths: 250 },
    { year: 2021, deaths: 230 },
    { year: 2022, deaths: 210 },
];

export default function DeathsTrend() {
    return (
        <div className="w-full h-64">
            <h3 className="text-lg font-semibold mb-2">Trend śmiertelnych wypadków</h3>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="deaths" stroke="#f87171" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}