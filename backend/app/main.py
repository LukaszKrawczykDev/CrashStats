from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from app.soap_server import soap_wsgi_app
from app.routers.auth_router import router as auth_router
from app.routers.accidents_router import router as accidents_router
from app.routers.data_router import router as data_router
from app.routers import test_isolation
from app.routers.stats import filters, accidents_by_month, deaths_trend, location_map, weather_chart, time_of_day
app = FastAPI()

app.include_router(auth_router)
app.include_router(accidents_router)
app.include_router(data_router)
app.include_router(test_isolation.router)
app.include_router(filters.router)
app.include_router(accidents_by_month.router)
app.include_router(deaths_trend.router)
app.include_router(location_map.router)
app.include_router(weather_chart.router)
app.include_router(time_of_day.router)

app.mount("/soap", WSGIMiddleware(soap_wsgi_app))

# routes...
#if accident_count == 0:
 #   print("🟡 Baza pusta – wgrywam dane")
    # os.system("python app/scripts/import_csv.py")
    # os.system("python app/scripts/fetch_weather.py")
#else:
 #   print("✅ Dane już są – nic nie robię")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)