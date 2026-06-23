from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import random

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Metrics Service Running"}

@app.get("/energy")
def get_metrics():
    return {
        "energy": random.randint(100, 400),
        "co2": random.randint(20, 80),
        "consumption": random.randint(200, 700)
    }