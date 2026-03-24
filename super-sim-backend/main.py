from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

app = FastAPI()

# -----------------------------
# CORS (แก้ปัญหา Next.js fetch)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Database จำลอง
# -----------------------------
tasks = []
results: Dict[int, dict] = {}

# -----------------------------
# Model
# -----------------------------
class CityRequest(BaseModel):
    city: str

class WorkerResult(BaseModel):
    task_id: int
    temperature: float
    humidity: float
    rain_probability: float


# -----------------------------
# User สั่ง Predict Weather
# -----------------------------
@app.post("/api/predict-weather")
def predict_weather(data: CityRequest):

    task_id = len(tasks) + 1

    task = {
        "task_id": task_id,
        "city": data.city,
        "status": "pending"
    }

    tasks.append(task)

    print(f"New task created : {data.city}")

    return {
        "task_id": task_id,
        "city": data.city
    }


# -----------------------------
# Worker ขอ Task
# -----------------------------
@app.get("/api/get-task")
def get_task():

    for task in tasks:

        if task["status"] == "pending":

            task["status"] = "processing"

            print(f"Task sent to worker : {task['city']}")

            return task

    return {"message": "no task"}


# -----------------------------
# Worker ส่ง Result
# -----------------------------
@app.post("/api/submit-result")
def submit_result(data: WorkerResult):

    results[data.task_id] = {
        "temperature": data.temperature,
        "humidity": data.humidity,
        "rain_probability": data.rain_probability
    }

    print(f"Result received : Task {data.task_id}")

    return {"message": "result saved"}


# -----------------------------
# Frontend ขอ Result
# -----------------------------
@app.get("/api/get-result/{task_id}")
def get_result(task_id: int):

    if task_id in results:

        return results[task_id]

    return {"message": "processing"}