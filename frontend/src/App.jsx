//App.jsx
import { useState } from "react";
import Header from "./components/Header";
import FilterBar from "./components/FilterBar";
import ChartGrid from "./components/charts/ChartGrid";

export default function App() {
    const [filters, setFilters] = useState({
        years: {
            2014: ["Wiosna", "Lato", "Jesień", "Zima"],
            2015: ["Wiosna", "Lato", "Jesień", "Zima"],
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