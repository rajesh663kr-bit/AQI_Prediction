from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

try:
    model = joblib.load("model.pkl")
    print("Model loaded successfully!")
except:
    model = None
    print("Model loading failed!")

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "#00e400", "Air quality is satisfactory."
    elif aqi <= 100:
        return "Moderate", "#ffff00", "Air quality is acceptable."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "#ff7e00", "Reduce prolonged outdoor activities."
    elif aqi <= 200:
        return "Unhealthy", "#ff0000", "Avoid long outdoor exposure."
    elif aqi <= 300:
        return "Very Unhealthy", "#8f3f97", "Serious health effects possible."
    else:
        return "Hazardous", "#7e0023", "Health warnings of emergency conditions."

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(data: dict):
    try:
        if model is None:
            return JSONResponse({"error": "Model not loaded"}, status_code=500)

        features = np.array([[data["PM25"], data["PM10"], data["NO2"], data["SO2"], data["CO"], data["O3"]]])

        aqi_pred = round(float(model.predict(features)[0]), 2)

        category, color, desc = get_aqi_category(aqi_pred)

        return {
            "success": True,
            "aqi": aqi_pred,
            "category": category,
            "color": color,
            "description": desc,
            "input": data
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
