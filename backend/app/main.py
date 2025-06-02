from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from app.soap_server import soap_wsgi_app
from app.routers.auth_router import router as auth_router
from app.routers.accidents_router import router as accidents_router
from app.routers.data_router import router as data_router
from app.routers import test_isolation
from app.routers.stats import AccidentsByMonth

app = FastAPI()

app.include_router(auth_router)
app.include_router(accidents_router)
app.include_router(data_router)
app.include_router(test_isolation.router)
app.include_router(AccidentsByMonth.router, prefix="/stats", tags=["Stats"])

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