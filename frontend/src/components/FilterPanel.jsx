// components/FilterPanel.jsx
export default function FilterPanel({ meta, filters, onChange }) {
    const toggle = (field, value) => {
        const current = Array.isArray(filters[field]) ? filters[field] : [];
        const updated = current.includes(value)
            ? current.filter(v => v !== value)
            : [...current, value];
        onChange({ ...filters, [field]: updated });
    };

    return (
        <div className="space-y-4">
            {Object.entries(meta).map(([field, values]) => (
                <div key={field}>
                    <div className="font-semibold">{field}</div>
                    <div className="flex flex-wrap gap-2">
                        {(values || []).map(value => (
                            <label key={value} className="text-sm">
                                <input
                                    type="checkbox"
                                    checked={(filters[field] || []).includes(value)}
                                    onChange={() => toggle(field, value)}
                                    className="mr-2"
                                />
                                {value}
                            </label>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}