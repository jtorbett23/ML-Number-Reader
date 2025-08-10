from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from use_model import predict_number
import numpy
import json

app = FastAPI(title="main app")

origins = [
    "https://jtorbett23.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def status():
    return {"Status": "UP"}

@app.post("/predict")
async def predict(request: Request):
    try:
        image_data = await request.json()
        image_data = json.loads(image_data)
        image_data = numpy.array(image_data, dtype=numpy.float16)
        prediction = predict_number(image_data)
        prediction = int(prediction)
    except:
        print("error")
    return prediction