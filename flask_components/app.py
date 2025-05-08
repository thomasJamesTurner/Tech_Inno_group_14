import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from flask import Flask, jsonify, render_template
from flighttracker.data_handling import flights_in_area, load_flights_from_db ,get_airport_weather
from flighttracker.map_link import make_map
import flighttracker.weather as Weather

app = Flask(__name__)

@app.route('/')
def dashboard():
    raw_flights = asyncio.run(flights_in_area("EGLL", 20))  # Live query
    inbound = []
    outbound = []
    for f in raw_flights:
        flight_data = {
            "flight": f.call_sign,  # callsign
            "airline": f.airline,  # first 3 letters
            "origin": "Unknown",  # origin not stored in db
            "etd": "Unknown",
            "destination": "Canada",
            "route": "NBA",
            "status": f.status,  # status
            "eta": f.eta if f.eta != None else "Delayed"  # mock logic
        }

        # Fake grouping logic: alternate between inbound/outbound
        if raw_flights.index(f) % 2 == 0:
            inbound.append(flight_data)
        else:
            outbound.append(flight_data)

    return render_template("dashboard.html", data={"inbound": inbound, "outbound": outbound})

@app.route("/flights-data")
def flights_data():
    flights = asyncio.run(flights_in_area("EGLL", 20))  # Live query

    inbound_data = []
    outbound_data = []

    for f in flights:
        flight_info = {
            "callsign": f.call_sign,
            "speed": f.speed,
            "altitude": f.altitude,
            "latitude": f.current_location.latitude,
            "longitude": f.current_location.longitude,
            "status": str(f.status),
            "eta": f.eta or "Unknown",
            "airline": f.airline,
            "destination": "EGLL",  # mock
            "origin": "Unknown"     # could be fetched if available
        }

        # Simulated logic: if altitude is low and descending → inbound
        if str(f.status) in ["Flight_Status.LANDING", "Flight_Status.GROUNDED"]:
            inbound_data.append(flight_info)
        else:
            outbound_data.append(flight_info)

    return jsonify({"inbound": inbound_data, "outbound": outbound_data})

@app.route("/weather-data")
@app.route("/weather-data")
def weather_data():
    print("getting weather")
    try:
        weather_info = asyncio.run(get_airport_weather("EGLL"))
        if weather_info:
            processed_info = []
            for hour in weather_info:
                processed_info.append({
                    "time": hour["time"],
                    "temperature": hour["temperature"],
                    "weathercode": hour["weathercode"],
                    "weather_description": Weather.weather.weather_code_to_text(hour["weathercode"]),
                    "weather_image": Weather.weather.weather_code_to_image(hour["weathercode"])
                })

            return jsonify({
                "current_weather": processed_info[0],
                "forecast": processed_info[1:] if len(processed_info) > 1 else []
            })
    except Exception as e:
        print(f"Error fetching weather data: {e}")
    return jsonify({"error": "Unable to fetch weather data"})

if __name__ == '__main__':
    make_map()
    app.run(debug=True)
