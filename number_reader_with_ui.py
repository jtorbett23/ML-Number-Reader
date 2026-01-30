from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from model.use_model import predict_number
import numpy
import json

app = FastAPI(title="main app")

@app.post("/predict")
async def predict(request: Request):
    try:
        image_data = await request.json()
        print(type(image_data))
        image_data = json.loads(image_data)
        print(type(image_data))
        image_data = numpy.array(image_data, dtype=numpy.float16)
        print(type(image_data))
        prediction = predict_number(image_data)
        print(prediction)
        prediction = int(prediction)
        print(type(prediction))
    except:
        print("error")
    return prediction

app.mount("/", StaticFiles(directory="ui", html=True), name="ui")