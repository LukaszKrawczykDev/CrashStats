// components/pages/ExportData.jsx
import { useState, useEffect } from "react";
import { useAuth } from "../features/auth/authContext";
import FilterPanel from "../components/FilterPanel";
import ExportButtons from "../components/ExportButtons";
import DataTable from "../components/DataTable";
import ColumnSelector from "../components/ColumnSelector";

export default function ExportData() {
    const { token } = useAuth();
    const [meta, setMeta] = useState({});
    const [filters, setFilters] = useState({});
    const [columns, setColumns] = useState([]);
    const [rows, setRows] = useState([]);

    // Ładowanie metadanych
    useEffect(() => {
        fetch("/api/data/filters/meta", {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then(res => {
                if (!res.ok) throw new Error(res.statusText);
                return res.json();
            })
            .then(data => {
                if (!data) throw new Error("Brak danych");
                setMeta(data);
                setFilters(Object.fromEntries(Object.keys(data).map(k => [k, []])));
                setColumns(Object.keys(data).slice(0, 15)); // Lub inna logika wyboru kolumn
            })
            .catch(err => {
                console.error("Błąd ładowania metadanych", err);
                setMeta({});
                setFilters({});
                setColumns([]);
            });
    }, [token]);

    // Podgląd danych
    useEffect(() => {
        if (columns.length === 0) return;

        fetch("/api/export", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ filters, columns, limit: 10 }),
        })
            .then(res => {
                if (!res.ok) throw new Error(res.statusText);
                return res.json();
            })
            .then(data => {
                if (!data?.rows) throw new Error("Nieprawidłowy format danych");
                setRows(data.rows);
            })
            .catch(err => {
                console.error("Błąd podglądu danych", err);
                setRows([]);
            });
    }, [filters, columns, token]);

    return (
        <div className="p-4 space-y-6">
            <h1 className="text-2xl font-bold">Eksport danych</h1>
            <FilterPanel meta={meta} filters={filters} onChange={setFilters} />
            <ColumnSelector meta={meta} columns={columns} onChange={setColumns} />
            <ExportButtons filters={filters} columns={columns} />
            <DataTable columns={columns} rows={rows} />
        </div>
    );
}