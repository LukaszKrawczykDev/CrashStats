// src/features/charts/VehicleTypeChart.jsx
import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";

const data = [
    { type: "Samochody osobowe", value: 320 },
    { type: "Ciężarówki", value: 90 },
    { type: "Motocykle", value: 70 },
    { type: "Autobusy", value: 30 },
    { type: "Inne", value: 15 },
];

const COLORS = ["#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8", "#1e40af"];

export default function VehicleTypeChart() {
    return (
        <div className="w-full h-64">
            <h3 className="text-lg font-semibold mb-2">Typ pojazdu a liczba wypadków</h3>
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        dataKey="value"
                        data={data}
                        outerRadius={80}
                        label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Pie>
                    <Tooltip />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}