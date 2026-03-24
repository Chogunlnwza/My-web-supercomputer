"use client"

import { useState } from "react"

export default function Home() {

  const [city, setCity] = useState("")
  const [temperature, setTemperature] = useState("")
  const [humidity, setHumidity] = useState("")
  const [rain, setRain] = useState("")

  const predictWeather = async (e:any) => {

    e.preventDefault()

    if (!city) return

    const res = await fetch("http://127.0.0.1:8000/api/predict-weather", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ city })
    })

    const data = await res.json()
    const task_id = data.task_id

    checkResult(task_id)
  }

  const checkResult = async (task_id:number) => {

    let done = false

    while (!done) {

      const res = await fetch(`http://127.0.0.1:8000/api/get-result/${task_id}`)
      const data = await res.json()

      if (data.temperature) {

        setTemperature(data.temperature.toFixed(2))
        setHumidity(data.humidity.toFixed(2))
        setRain(data.rain_probability.toFixed(2))

        done = true
      }

      await new Promise(r => setTimeout(r, 2000))
    }
  }

  return (

    <div style={{
      background:"black",
      color:"white",
      height:"100vh",
      display:"flex",
      flexDirection:"column",
      justifyContent:"center",
      alignItems:"center",
      fontFamily:"monospace"
    }}>

      <h1>Supercomputer Weather Prediction</h1>

      <form onSubmit={predictWeather}>

        <input
  type="text"
  placeholder="Enter city"
  value={city}
  onChange={(e)=>setCity(e.target.value)}
  style={{
    padding:"10px",
    marginTop:"20px",
    width:"250px",
    background:"black",
    color:"white",
    border:"1px solid white"
  }}
/>

        <br/>

        <button
          type="submit"
          style={{
            marginTop:"20px",
            padding:"10px"
          }}
        >
          Predict Weather
        </button>

      </form>

      <div style={{marginTop:"40px"}}>

        <h2>Result</h2>

        <p>Temperature : {temperature} °C</p>
        <p>Humidity : {humidity} %</p>
        <p>Rain Chance : {rain} %</p>

      </div>

    </div>
  )
}