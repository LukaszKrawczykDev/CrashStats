// src/features/charts/UserTypeChart.jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
    { type: "Pieszy", count: 87 },
    { type: "Rowerzysta", count: 45 },
    { type: "Motocyklista", count: 30 },
    { type: "Kierowca", count: 120 },
];

export default function UserTypeChart() {
    return (
        <div className="w-full h-64">
            <h3 className="text-lg font-semibold mb-2">Uczestnicy wypadków</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <XAxis dataKey="type" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#3b82f6" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}