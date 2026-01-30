from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from model.use_model import predict_digit
import numpy
import json
from dotenv import load_dotenv
import os

load_dotenv()

origins = os.getenv("ORIGINS", "").split(",")

print(origins)

app = FastAPI(title="main app")

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
        prediction = predict_digit(image_data)
        prediction = int(prediction)
    except:
        print("error")
    return prediction