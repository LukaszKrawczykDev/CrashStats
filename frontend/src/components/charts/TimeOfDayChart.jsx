// src/features/charts/TimeOfDayChart.jsx
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

const data = [
    { time: "Noc", kolizje: 20, zderzenia: 10 },
    { time: "Rano", kolizje: 30, zderzenia: 15 },
    { time: "Dzień", kolizje: 50, zderzenia: 25 },
    { time: "Wieczór", kolizje: 40, zderzenia: 30 },
];

export default function TimeOfDayChart() {
    return (
        <div className="w-full h-64">
            <h3 className="text-lg font-semibold mb-2">Pora dnia a typ wypadku</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="kolizje" stackId="a" fill="#60a5fa" />
                    <Bar dataKey="zderzenia" stackId="a" fill="#3b82f6" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}