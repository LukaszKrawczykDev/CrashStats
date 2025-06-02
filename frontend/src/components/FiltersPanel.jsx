import { useState } from "react";

const years = [2021, 2022, 2023, 2024];
const months = [
    { num: 1, name: "Styczeń" }, { num: 2, name: "Luty" }, { num: 3, name: "Marzec" },
    { num: 4, name: "Kwiecień" }, { num: 5, name: "Maj" }, { num: 6, name: "Czerwiec" },
    { num: 7, name: "Lipiec" }, { num: 8, name: "Sierpień" }, { num: 9, name: "Wrzesień" },
    { num: 10, name: "Październik" }, { num: 11, name: "Listopad" }, { num: 12, name: "Grudzień" },
];

export default function FiltersPanel({ filters, onChange, onClose }) {
    const [selectedYears, setSelectedYears] = useState(filters.year || []);
    const [selectedMonths, setSelectedMonths] = useState(filters.month || []);

    const toggle = (value, list, setList) => {
        if (list.includes(value)) {
            setList(list.filter((v) => v !== value));
        } else {
            setList([...list, value]);
        }
    };

    const applyFilters = () => {
        onChange({ ...filters, year: selectedYears, month: selectedMonths });
        onClose();
    };

    const clearFilters = () => {
        setSelectedYears([]);
        setSelectedMonths([]);
        onChange({ year: [], month: [], mode: "all" });
        onClose();
    };

    return (
        <div className="bg-gray-100 p-4 mt-4 rounded shadow-md">
            <h3 className="font-semibold text-lg mb-2">Filtruj dane</h3>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <h4 className="font-semibold">Lata</h4>
                    {years.map((year) => (
                        <label key={year} className="block">
                            <input
                                type="checkbox"
                                checked={selectedYears.includes(year)}
                                onChange={() => toggle(year, selectedYears, setSelectedYears)}
                            />{" "}
                            {year}
                        </label>
                    ))}
                </div>

                <div>
                    <h4 className="font-semibold">Miesiące</h4>
                    {months.map(({ num, name }) => (
                        <label key={num} className="block">
                            <input
                                type="checkbox"
                                checked={selectedMonths.includes(num)}
                                onChange={() => toggle(num, selectedMonths, setSelectedMonths)}
                            />{" "}
                            {name}
                        </label>
                    ))}
                </div>
            </div>

            <div className="flex justify-end gap-2">
                <button onClick={clearFilters} className="bg-gray-400 text-white px-3 py-2 rounded">
                    Wyczyść
                </button>
                <button onClick={applyFilters} className="bg-blue-600 text-white px-3 py-2 rounded">
                    Zastosuj
                </button>
            </div>
        </div>
    );
}