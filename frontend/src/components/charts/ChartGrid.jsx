// src/components/charts/ChartGrid.jsx
import React, { useState } from "react";
import ChartCard from "../ChartCard";
import ChartModal from "./ChartModal";

import AccidentsByMonth from "./AccidentsByMonth";
import DeathsTrend from "./DeathsTrend";
import LocationMap from "./LocationMap";
import WeatherChart from "./WeatherChart";
import SeverityAvgChart from "./SeverityAvgChart";
import TimeOfDayChart from "./TimeOfDayChart";
import UserTypeChart from "./UserTypeChart";
import RoadTypeChart from "./VehicleTypeChart.jsx"; // ok

const chartComponents = [
    { title: "Wypadki miesięcznie", Component: AccidentsByMonth },
    { title: "Trend zgonów", Component: DeathsTrend },
    { title: "Mapa lokalizacji", Component: LocationMap },
    { title: "Pogoda a wypadki", Component: WeatherChart },
    { title: "Średnia ciężkość obrażeń", Component: SeverityAvgChart },
    { title: "Pora dnia", Component: TimeOfDayChart },
    { title: "Typ uczestnika", Component: UserTypeChart },
    { title: "Rodzaj drogi", Component: RoadTypeChart },
];

// 💡 PRZYJMIJ filters jako props!
export default function ChartGrid({ filters }) {
    const [modalChart, setModalChart] = useState(null);

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {chartComponents.map(({ title, Component }, idx) => (
                <ChartCard key={idx} title={title} onExpand={() => setModalChart({ title, Component })}>
                    <Component filters={filters} />
                </ChartCard>
            ))}

            {modalChart && (
                <ChartModal
                    title={modalChart.title}
                    isOpen={!!modalChart}
                    onClose={() => setModalChart(null)}
                >
                    <modalChart.Component filters={filters} />
                </ChartModal>
            )}
        </div>
    );
}