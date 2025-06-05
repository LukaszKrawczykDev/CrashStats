// App.jsx
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import FilterBar from "./components/FilterBar";
import ChartGrid from "./components/charts/ChartGrid";
import ExportData from "./pages/ExportData";

export default function App() {
    const [filters, setFilters] = useState({
        years: {
            2014: ["Wiosna", "Lato", "Jesień", "Zima"],
            2015: ["Wiosna", "Lato", "Jesień", "Zima"],
        },
    });

    return (
        <Router>
            <Header />
            <main className="p-4">
                <Routes>
                    <Route
                        path="/"
                        element={
                            <>
                                <FilterBar filters={filters} onChange={setFilters} />
                                <ChartGrid filters={filters} />
                            </>
                        }
                    />
                    <Route path="/export" element={<ExportData />} />
                </Routes>
            </main>
        </Router>
    );
}