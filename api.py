from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from use_model import predict_number
import numpy
import json
#TODO
# Only allow requests from the ui
# Try saving the screenshot to a local python file and have the app read from that instead of passing the content as an api request
# find a way to make sure tensorflow is setup prior to server
# lock dependencies 
# fix showing as it is not showing calcutating on render consistently
# current deploy delay on render is 6mins can we speed this up
# update the ui and have controls on it
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