// App.jsx
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import FilterBar from "./components/FilterBar";
import ChartGrid from "./components/charts/ChartGrid";
import ExportPage from "./pages/ExportPage.jsx";
import ImportPage from "./pages/ImportPage.jsx";

export default function App() {
    const [filters, setFilters] = useState();

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
                    <Route path="/export" element={<ExportPage />} />
                    <Route path="/import" element={<ImportPage />} />
                </Routes>

            </main>
        </Router>
    );
}