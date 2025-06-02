// src/features/charts/SeverityAvgChart.jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
    { month: "Sty", obrażenia: 1.2, zgony: 0.3 },
    { month: "Lut", obrażenia: 1.4, zgony: 0.2 },
    { month: "Mar", obrażenia: 1.1, zgony: 0.5 },
    { month: "Kwi", obrażenia: 1.3, zgony: 0.4 },
];

export default function SeverityAvgChart() {
    return (
        <div className="w-full h-64">
            <h3 className="text-lg font-semibold mb-2">Średnia liczba ofiar na wypadek</h3>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="obrażenia" stroke="#3b82f6" />
                    <Line type="monotone" dataKey="zgony" stroke="#ef4444" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}