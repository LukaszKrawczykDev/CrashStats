import { useState } from "react";
import Header from "./components/Header";
import FilterBar from "./components/FilterBar";
import ChartGrid from "./components/charts/ChartGrid";

export default function App() {
    const [filters, setFilters] = useState({
        years: {
            2021: ["Wiosna", "Lato", "Jesień", "Zima"],
            2022: ["Wiosna", "Lato", "Jesień", "Zima"],
            2023: ["Wiosna", "Lato", "Jesień", "Zima"],
            2024: ["Wiosna", "Lato", "Jesień", "Zima"],
        },
    });

    return (
        <div>
            <Header />
            <main className="p-4">
                <FilterBar filters={filters} onChange={setFilters} />
                <ChartGrid filters={filters} />
            </main>
        </div>
    );
}