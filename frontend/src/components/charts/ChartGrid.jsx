// src/components/charts/ChartGrid.jsx
import React, { useState } from "react";
import ChartCard from "../ChartCard";
import ChartModal from "./ChartModal";

import AccidentsByMonth from "./AccidentsByMonth";
import DeathsTrend from "./DeathsTrend";
import LocationMap from "./LocationMap";
import WeatherChart from "./WeatherChart";
import TimeOfDayChart from "./TimeOfDayChart";
import UserTypeWeatherChart from "./UserTypeWeatherChart.jsx";

const chartComponents = [
    { title: "Wypadki miesięcznie", Component: AccidentsByMonth },
    { title: "Trend śmiertelnych wypadków", Component: DeathsTrend },
    { title: "Mapa lokalizacji", Component: LocationMap },
    { title: "Pogoda a wypadki", Component: WeatherChart },
    { title: "Pora dnia", Component: TimeOfDayChart },
    { title: "Typ uczestnika", Component: UserTypeWeatherChart },

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
                    <modalChart.Component filters={filters} expanded={true} />
                </ChartModal>
            )}
        </div>
    );
}