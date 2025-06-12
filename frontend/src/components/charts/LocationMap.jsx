import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Checkbox } from "../ui/checkbox";

const injuryColors = {
    Fatal: "#ef4444",
    "Non-incapacitating": "#f59e0b",
    "No injury/unknown": "#3b82f6",
    Incapacitating: "#10b981",
    OTHER: "#6b7280",
};

const allowedInjuryTypes = Object.keys(injuryColors);

const ALLOWED_PRIMARY_FACTORS = [
    "OTHER (ENVIRONMENTAL) - EXPLAIN IN NARR",
    "TIRE FAILURE OR DEFECTIVE",
    "ANIMAL/OBJECT IN ROADWAY",
    "DRIVER ASLEEP OR FATIGUED",
    "OVERCORRECTING/OVERSTEERING",
    "IMPROPER TURNING",
    "ENGINE FAILURE OR DEFECTIVE",
    "DRIVER DISTRACTED - EXPLAIN IN NARRATIVE",
    "OTHER (DRIVER) - EXPLAIN IN NARRATIVE",
    "OVERSIZE/OVERWEIGHT LOAD",
    "UNSAFE LANE MOVEMENT",
    "FAILURE TO YIELD RIGHT OF WAY",
    "ROADWAY SURFACE CONDITION",
    "RAN OFF ROAD RIGHT",
    "PEDESTRIAN ACTION",
    "INSECURE/LEAKY LOAD",
    "OTHER (VEHICLE) - EXPLAIN IN NARRATIVE",
    "CELL PHONE USAGE",
    "HOLES/RUTS IN SURFACE",
    "ACCELERATOR FAILURE OR DEFECTIVE",
    "FOLLOWING TOO CLOSELY",
    "OBSTRUCTION NOT MARKED",
    "OTHER LIGHTS DEFECTIVE",
    "SPEED TOO FAST FOR WEATHER CONDITIONS",
    "DISREGARD SIGNAL/REG SIGN",
    "WRONG WAY ON ONE WAY",
    "BRAKE FAILURE OR DEFECTIVE",
    "HEADLIGHT DEFECTIVE OR NOT ON",
    "STEERING FAILURE",
    "UNSAFE BACKING",
    "TOW HITCH FAILURE",
    "DRIVER ILLNESS",
    "IMPROPER LANE USAGE",
    "VIEW OBSTRUCTED",
    "IMPROPER PASSING",
    "TRAFFIC CONTROL INOPERATIVE/MISSING/OBSC",
    "LEFT OF CENTER",
    "OTHER TELEMATICS IN USE",
    "UNSAFE SPEED",
    "OTHER",
];

export default function LocationMap({ expanded = false }) {
    const [data, setData] = useState([]);
    const [injuryFilter, setInjuryFilter] = useState(new Set(allowedInjuryTypes));
    const [primaryFilter, setPrimaryFilter] = useState(new Set(["OTHER"]));

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await fetch("/api/stats/location-map", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        injury_types: Array.from(injuryFilter),
                        primary_factors: Array.from(primaryFilter),
                    }),
                });
                const json = await res.json();
                setData(json);
            } catch (e) {
                console.error("Błąd mapy:", e);
            }
        };
        fetchData();
    }, [injuryFilter, primaryFilter]);

    const toggle = (set, type) => {
        const copy = new Set(set);
        if (copy.has(type)) copy.delete(type);
        else copy.add(type);
        return copy;
    };

    return (
        <div className="w-full h-[32rem] relative">
            <MapContainer center={[39.19, -86.57]} zoom={11} className="w-full h-full z-0 rounded-xl">
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                {data.map((d, i) => (
                    <Marker
                        key={i}
                        position={[d.lat, d.lng]}
                        icon={L.divIcon({
                            className: "",
                            html: `<div style="background:${injuryColors[d.injury_type] || injuryColors.OTHER};width:10px;height:10px;border-radius:50%"></div>`
                        })}
                    >
                        <Popup>
                            <div className="text-sm">
                                <div><strong>{d.injury_type}</strong> - {d.primary_factor}</div>
                                <div>{d.collision_type}</div>
                                <div>{d.street1} {d.street2}</div>
                                <div>{d.day}.{d.month}.{d.year} {d.hour}:00 {d.is_weekend ? "(Weekend)" : ""}</div>
                                <hr className="my-1" />
                                <div>🌡 Temp: {d.temperature}°C</div>
                                <div>☁️ Chmury: {d.clouds} | {d.category}</div>
                                <div>🌧 Rain24h: {d.rain_24h}mm</div>
                                <div>❄️ Snow24h: {d.snow_24h}mm</div>
                                <div>💨 Wiatr: {d.wind_speed}km/h ({d.wind_deg}°)</div>
                                <div>🛣 {d.road_condition}</div>
                            </div>
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>

            {expanded && (
                <div className="absolute top-4 right-4 bg-white p-4 rounded-xl shadow z-[1000] max-h-[90%] overflow-auto w-80">
                    <h4 className="font-bold mb-2">Rodzaj urazu</h4>
                    {allowedInjuryTypes.map((type) => (
                        <div key={type} className="flex items-center gap-2 mb-1">
                            <Checkbox checked={injuryFilter.has(type)} onChange={() => setInjuryFilter(toggle(injuryFilter, type))} />
                            <span style={{ color: injuryColors[type] }}>{type}</span>
                        </div>
                    ))}
                    <hr className="my-2" />
                    <h4 className="font-bold mb-2">Czynnik główny</h4>
                    {ALLOWED_PRIMARY_FACTORS.map((type) => (
                        <div key={type} className="flex items-center gap-2 mb-1">
                            <Checkbox checked={primaryFilter.has(type)} onChange={() => setPrimaryFilter(toggle(primaryFilter, type))} />
                            <span>{type}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}