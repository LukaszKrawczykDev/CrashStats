from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.stats import filters, accidents_by_month, deaths_trend, location_map, weather_chart, time_of_day, user_weather_chart
from app.routers import export_router
from app.routers import import_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(filters.router)
app.include_router(accidents_by_month.router)
app.include_router(deaths_trend.router)
app.include_router(location_map.router)
app.include_router(weather_chart.router)
app.include_router(time_of_day.router)
app.include_router(user_weather_chart.router)
app.include_router(export_router.router)
app.include_router(import_router.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)