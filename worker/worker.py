import requests
import time
import random

MASTER = "http://127.0.0.1:8000"

def simulate_weather(city):

    temperature = random.uniform(25,35)
    humidity = random.uniform(60,90)
    rain = random.uniform(0,100)

    return temperature, humidity, rain


while True:

    try:

        r = requests.get(f"{MASTER}/api/get-task")
        task = r.json()

        if "task_id" not in task:

            time.sleep(2)
            continue

        city = task["city"]
        task_id = task["task_id"]

        print(f"Processing weather for {city}")

        temp, hum, rain = simulate_weather(city)

        result = {
            "task_id": task_id,
            "temperature": temp,
            "humidity": hum,
            "rain_probability": rain
        }

        requests.post(f"{MASTER}/api/submit-result", json=result)

        print("Result sent to master")

    except:

        print("Connection error")

    time.sleep(1)