from asgiref.wsgi import WsgiToAsgi
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from flask import Flask, jsonify, render_template
from flighttracker.data_handling import flights_in_area, load_flights_from_db ,get_airport_weather
from flighttracker.map_link import make_map
import flighttracker.weather as Weather

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

def parse_flights(data):
    inbound = []
    outbound = []
    if isinstance(data[0],tuple):
        for f in data:
            flight_data = {
                "flight": f[2],  # callsign
                "airline": f[2][:3],  # first 3 letters
                "origin": "Unknown",  # origin not stored in db
                "etd": "Unknown",
                "destination": "Canada",
                "route": "NBA",
                "status": f[7],  # status
                "eta": "On time" if "On time" in f[2] else "Delayed"  # mock logic
        }
            if data.index(f) % 2 == 0:
                inbound.append(flight_data)
            else:
                outbound.append(flight_data)
    else:
        for f in data:
            flight_data = {
                "flight": f.callsign,  # callsign
                "airline": f.airline,  # first 3 letters
                "origin": "Unknown",  # origin not stored in db
                "etd": "Unknown",
                "destination": "Canada",
                "route": "NBA",
                "status": f.status,  # status
                "eta": f.eta if f.eta != None else "Delayed"  # mock logic
            }
            if data.index(f) % 2 == 0:
                inbound.append(flight_data)
            else:
                outbound.append(flight_data)
    return (inbound,outbound)


@app.route('/')
def dashboard():
    raw_flights = flights_in_area("EGLL", 20)  # Live query
    #raw_flights = load_flights_from_db()
    flights = parse_flights(raw_flights)

    return render_template("dashboard.html", data={"inbound": flights[0], "outbound": flights[1]})

@app.route("/flights-data")
def flights_data():
    raw_flights = flights_in_area("EGLL", 20)  # Live query
    raw_flights = load_flights_from_db()
    flights = parse_flights(raw_flights)
    
    

    return jsonify({"inbound": flights[0], "outbound": flights[1]})

@app.route("/weather-data")
async def weather_data():
    print("getting weather")
    try:
        weather_info = await get_airport_weather("EGLL")
        if weather_info:
            for hour in weather_info:
                hour["weathercode"] = Weather.weather.weather_code_to_text(hour["weathercode"])
            return jsonify(weather_info)
        else:
            return jsonify([]), 404
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    print(get_airport_weather("EGLL"))
    make_map()
    app.run(debug=True)
