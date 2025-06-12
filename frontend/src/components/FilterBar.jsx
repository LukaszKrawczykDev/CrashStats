import React, { useEffect, useState } from "react";

const seasonMap = {
    Wiosna: [3, 4, 5],
    Lato: [6, 7, 8],
    Jesień: [9, 10, 11],
    Zima: [12, 1, 2],
};

const getSeasonsForMonths = (months) => {
    const seasons = new Set();
    months.forEach((m) => {
        for (const [season, values] of Object.entries(seasonMap)) {
            if (values.includes(m)) {
                seasons.add(season);
            }
        }
    });
    return Array.from(seasons);
};

export default function FilterBar({ filters, onChange }) {
    const [open, setOpen] = useState(false);
    const [availableYears, setAvailableYears] = useState({});
    const [localFilters, setLocalFilters] = useState({ years: {} });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("/api/stats/filters/meta")
            .then((res) => res.json())
            .then((data) => {
                setAvailableYears(data);

                const initial = {};
                for (const [year, months] of Object.entries(data)) {
                    initial[year] = getSeasonsForMonths((months || []).map(Number))
                }

                setLocalFilters({ years: initial });
                onChange({ years: initial });
                setLoading(false);
            });
    }, []);

    const toggleYear = (year) => {
        setLocalFilters((prev) => {
            const updated = { ...prev.years };
            if (updated[year]) {
                delete updated[year];
            } else {
                const months = availableYears[year].map(Number);
                updated[year] = getSeasonsForMonths(months);
            }
            return { years: updated };
        });
    };

    const toggleSeason = (year, season) => {
        setLocalFilters((prev) => {
            const updated = { ...prev.years };
            const selected = updated[year] || [];
            if (selected.includes(season)) {
                updated[year] = selected.filter((s) => s !== season);
            } else {
                updated[year] = [...selected, season];
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
        for (const [year, months] of Object.entries(availableYears)) {
            reset[year] = getSeasonsForMonths(months.map(Number));
        }
        setLocalFilters({ years: reset });
        onChange({ years: reset });
        setOpen(false);
    };

    return (
        <div className="sticky top-16 z-40 bg-white shadow px-4 py-2 mb-4">
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded shadow"
                onClick={() => setOpen(!open)}
            >
                Filtry
            </button>

            {open && !loading && (
                <div className="bg-gray-100 mt-4 p-4 rounded shadow">
                    {Object.entries(availableYears).map(([year, months]) => (
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
                                    {getSeasonsForMonths(months.map(Number)).map((season) => (
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