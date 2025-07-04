import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import FilterBar from "./components/FilterBar";
import ChartGrid from "./components/charts/ChartGrid.jsx";
import ExportPage from "./pages/ExportPage.jsx";
import ImportPage from "./pages/ImportPage.jsx";
import SoapStats from "./pages/SoapStats";

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
                    <Route path="/soap-stats" element={<SoapStats />} />
                </Routes>

            </main>
        </Router>
    );
}