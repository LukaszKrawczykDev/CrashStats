import uvicorn
from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.accidents_router import router as accidents_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(accidents_router)
# routes...
#if accident_count == 0:
 #   print("🟡 Baza pusta – wgrywam dane")
    # os.system("python app/scripts/import_csv.py")
    # os.system("python app/scripts/fetch_weather.py")
#else:
 #   print("✅ Dane już są – nic nie robię")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)