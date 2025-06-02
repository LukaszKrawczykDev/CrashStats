// src/components/charts/ChartCard.jsx
import React from "react";

export default function ChartCard({ title, children, onExpand }) {
    return (
        <div className="bg-white rounded-xl shadow p-4 relative">
            <h3 className="text-lg font-semibold mb-2">{title}</h3>
            <div>{children}</div>
            <button
                onClick={onExpand}
                className="absolute top-2 right-2 text-sm text-blue-500 hover:underline"
            >
                Powiększ
            </button>
        </div>
    );
}