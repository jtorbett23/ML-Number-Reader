from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="main app")

app.mount("/", StaticFiles(directory="ui", html=True), name="ui")