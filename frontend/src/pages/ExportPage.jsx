import { useEffect, useState } from 'react';
import { Checkbox } from '../components/ui/checkbox';

const API = import.meta.env.VITE_API_URL;

export default function ExportPage() {
    const [years, setYears] = useState([]);
    const [selected, setSelected] = useState([]);
    const [format, setFormat] = useState('json');
    const [previewText, setPreviewText] = useState('');

    useEffect(() => { fetchYears() }, []);
    useEffect(() => { fetchPreview() }, [selected, format]);

    async function fetchYears() {
        try {
            const res = await fetch(`${API}/export/years`);
            const { years } = await res.json();
            setYears(years);
        } catch (e) { console.error(e) }
    }

    async function fetchPreview() {
        try {
            const qs = new URLSearchParams();
            selected.forEach(y => qs.append('years', y));
            qs.set('format', format);
            qs.set('preview', 'true');

            const res = await fetch(`${API}/export/data?${qs.toString()}`);
            const text = await res.text();
            setPreviewText(text);
        } catch (e) { console.error(e) }
    }

    const toggle = y =>
        setSelected(s => s.includes(y) ? s.filter(x => x !== y) : [...s, y]);

    const download = async () => {
        const qs = new URLSearchParams();
        selected.forEach(y => qs.append('years', y));
        qs.set('format', format);
        const url = `${API}/export/data?${qs.toString()}`;

        window.location.href = url;
    };

    return (
        <div className="p-4">
            <h2 className="text-xl font-semibold mb-4">Eksport danych</h2>

            <div className="mb-4">
                <h3 className="font-semibold">Lata:</h3>
                <div className="flex flex-wrap gap-4 mt-2">
                    {years.map(y => (
                        <label key={y} className="flex items-center space-x-2">
                            <Checkbox checked={selected.includes(y)} onChange={() => toggle(y)} />
                            <span>{y}</span>
                        </label>
                    ))}
                </div>
            </div>

            <div className="mb-4">
                <span className="font-semibold">Format:</span>
                <select
                    className="ml-2 p-1 border rounded"
                    value={format}
                    onChange={e => setFormat(e.target.value)}
                >
                    <option value="json">JSON</option>
                    <option value="yaml">YAML</option>
                    <option value="xml">XML</option>
                </select>
            </div>

            <button
                className="bg-blue-600 text-white px-4 py-2 rounded"
                onClick={download}
            >
                Eksportuj
            </button>

            <div className="mt-6">
                <h3 className="font-semibold">Podgląd (10 rekordów):</h3>
                <pre className="mt-2 bg-gray-100 p-2 rounded overflow-auto whitespace-pre-wrap">
          {previewText}
        </pre>
            </div>
        </div>
    );
}