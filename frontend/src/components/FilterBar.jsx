// src/components/FilterBar.jsx
import React, { useState } from "react";

const seasons = ["Wiosna", "Lato", "Jesień", "Zima"];
const availableYears = [2021, 2022, 2023, 2024];

export default function FilterBar({ filters, onChange }) {
    const [open, setOpen] = useState(false);
    const [localFilters, setLocalFilters] = useState(filters);

    const toggleYear = (year) => {
        setLocalFilters((prev) => {
            const updated = { ...prev.years };
            if (updated[year]) {
                delete updated[year];
            } else {
                updated[year] = [...seasons];
            }
            return { years: updated };
        });
    };

    const toggleSeason = (year, season) => {
        setLocalFilters((prev) => {
            const updated = { ...prev.years };
            const existing = updated[year] || [];
            if (existing.includes(season)) {
                updated[year] = existing.filter((s) => s !== season);
            } else {
                updated[year] = [...existing, season];
            }
            return { years: updated };
        });
    };

    const applyFilters = () => {
        onChange(localFilters);
        setOpen(false);
    };

    const clearFilters = () => {
        const reset = {};
        availableYears.forEach((year) => (reset[year] = [...seasons]));
        onChange({ years: reset });
        setLocalFilters({ years: reset });
        setOpen(false);
    };

    return (
        <div className="sticky top-16 z-40 bg-white shadow px-4 py-2 mb-4">
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded shadow"
                onClick={() => setOpen((prev) => !prev)}
            >
                Filtry
            </button>

            {open && (
                <div className="bg-gray-100 mt-4 p-4 rounded shadow">
                    {availableYears.map((year) => (
                        <div key={year} className="mb-2">
                            <label className="font-semibold">
                                <input
                                    type="checkbox"
                                    checked={!!localFilters.years[year]}
                                    onChange={() => toggleYear(year)}
                                    className="mr-2"
                                />
                                {year}
                            </label>
                            {localFilters.years[year] && (
                                <div className="ml-6 mt-1 flex flex-wrap gap-2">
                                    {seasons.map((season) => (
                                        <label key={season} className="text-sm">
                                            <input
                                                type="checkbox"
                                                checked={localFilters.years[year].includes(season)}
                                                onChange={() => toggleSeason(year, season)}
                                                className="mr-1"
                                            />
                                            {season}
                                        </label>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}

                    <div className="mt-4 flex gap-2">
                        <button
                            className="bg-green-600 text-white px-4 py-2 rounded"
                            onClick={applyFilters}
                        >
                            Zastosuj filtry
                        </button>
                        <button
                            className="bg-gray-400 text-white px-4 py-2 rounded"
                            onClick={clearFilters}
                        >
                            Wyczyść filtry
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}