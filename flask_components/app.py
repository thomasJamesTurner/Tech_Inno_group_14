import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from flask import Flask, jsonify, render_template
from flighttracker.data_handling import flights_in_area, load_flights_from_db

app = Flask(__name__)

@app.route('/')
def dashboard():
    raw_flights = load_flights_from_db(limit=10)
    
    inbound = []
    outbound = []
    for row in raw_flights:
        flight_data = {
            "flight": row[2],  # callsign
            "airline": row[2][:3],  # first 3 letters
            "origin": "Unknown",  # origin not stored in db
            "etd": "Unknown",
            "destination": "New York" if "JNR" in row[2] else "Canada",  # fake logic for demo
            "route": "JNR" if "JNR" in row[2] else "NBA",  # fake logic
            "status": row[7],  # status
            "eta": "On time" if "On time" in row[2] else "Delayed"  # mock logic
        }

        # Fake grouping logic: alternate between inbound/outbound
        if raw_flights.index(row) % 2 == 0:
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



if __name__ == '__main__':
    app.run(debug=True)
