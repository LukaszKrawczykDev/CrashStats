export default function ColumnSelector({ allColumns = [], selected = [], onChange }) {
    const toggle = (col) => {
        const current = Array.isArray(selected) ? selected : [];
        const updated = current.includes(col)
            ? current.filter(c => c !== col)
            : [...current, col];
        onChange(updated);
    };

    return (
        <div className="space-y-2">
            <div className="font-semibold">Wybierz kolumny</div>
            <div className="flex flex-wrap gap-2">
                {(allColumns || []).map(col => (
                    <label key={col} className="text-sm">
                        <input
                            type="checkbox"
                            checked={(selected || []).includes(col)}
                            onChange={() => toggle(col)}
                            className="mr-2"
                        />
                        {col}
                    </label>
                ))}
            </div>
        </div>
    );
}