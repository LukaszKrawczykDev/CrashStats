export default function DataTable({ rows = [] }) {
    if (!rows || !rows.length) return <p className="text-gray-500">Brak danych do wyświetlenia</p>;

    const columns = rows[0] ? Object.keys(rows[0]) : [];


    return (
        <div className="overflow-auto border rounded">
            <table className="min-w-full text-sm text-left border-collapse">
                <thead>
                <tr className="bg-gray-200">
                    {columns.map(col => (
                        <th key={col} className="px-4 py-2 border">{col}</th>
                    ))}
                </tr>
                </thead>
                <tbody>
                {rows.map((row, i) => (
                    <tr key={i} className="odd:bg-white even:bg-gray-50">
                        {columns.map(col => (
                            <td key={col} className="px-4 py-2 border">{row[col]}</td>
                        ))}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}