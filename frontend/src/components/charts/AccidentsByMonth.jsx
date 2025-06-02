// src/features/charts/AccidentsByMonth.jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
    { month: "Styczeń", count: 30 },
    { month: "Luty", count: 22 },
    { month: "Marzec", count: 27 },
    { month: "Kwiecień", count: 35 },
    { month: "Maj", count: 40 },
    { month: "Czerwiec", count: 38 },
    { month: "Lipiec", count: 44 },
    { month: "Sierpień", count: 41 },
    { month: "Wrzesień", count: 36 },
    { month: "Październik", count: 32 },
    { month: "Listopad", count: 28 },
    { month: "Grudzień", count: 25 },
];

export default function AccidentsByMonth() {
    return (
        <div className="w-full h-64">
            <h3 className="text-lg font-semibold mb-2">Wypadki według miesiąca</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#60a5fa" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}