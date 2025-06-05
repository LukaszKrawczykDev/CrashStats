import { useAuth } from "../features/auth/authContext";

export default function ExportButtons({ filters, columns }) {
    const { token } = useAuth();

    const handleExport = async (format) => {
        try {
            const res = await fetch("/api/export", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ filters, columns, format }),
            });

            if (!res.ok) throw new Error("Export failed");

            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `export.${format}`;
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (e) {
            console.error("Export error:", e);
        }
    };

    return (
        <div className="flex gap-4 my-4">
            {["json", "yaml", "xml"].map(format => (
                <button
                    key={format}
                    onClick={() => handleExport(format)}
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                    Eksportuj ({format.toUpperCase()})
                </button>
            ))}
        </div>
    );
}