from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
import joblib

app = FastAPI()

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model (kept for academic requirement)
model_path = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(model_path) if os.path.exists(model_path) else None

# ---------- Static & Templates ----------
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ---------- API KEY ----------
API_KEY = "PASTE_YOUR_OPENWEATHER_API_KEY_HERE"

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/aqi/{city}")
def get_aqi(city: str):

    # ---------- GEO API ----------
    geo_url = (
        "https://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={API_KEY}"
    )

    geo_response = requests.get(geo_url)

    # ❌ API request failed
    if geo_response.status_code != 200:
        return {"error": "Geo API request failed"}

    geo_data = geo_response.json()

    # ❌ City not found OR API error
    if not isinstance(geo_data, list) or len(geo_data) == 0:
        return {"error": "City not found or invalid API key"}

    lat = geo_data[0].get("lat")
    lon = geo_data[0].get("lon")

    if lat is None or lon is None:
        return {"error": "Location coordinates not available"}

    # ---------- AQI API ----------
    aqi_url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    aqi_response = requests.get(aqi_url)

    if aqi_response.status_code != 200:
        return {"error": "AQI API request failed"}

    aqi_data = aqi_response.json()

    if "list" not in aqi_data or len(aqi_data["list"]) == 0:
        return {"error": "AQI data not available"}

    aqi_value = aqi_data["list"][0]["main"]["aqi"]

    status_map = {
        1: "Good 😊",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor ☠️"
    }

    return {
        "city": city.title(),
        "aqi": aqi_value,
        "status": status_map.get(aqi_value, "Unknown")
    }
