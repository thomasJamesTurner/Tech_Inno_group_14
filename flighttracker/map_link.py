import folium
from pathlib import Path
from flighttracker.flight import Flight, Flight_Status  # Adjust import if needed
import flighttracker.location as location
from flighttracker.data_handling import get_airport_coordinates

def make_map():
    coords = get_airport_coordinates("EGLL")
    # Simulated flight data — replace this with your real `flights` list
    flights = [
        Flight("SWR5QD", 0.06, "Unknown", location.Location(-0.45, 51.47),coords),
        Flight("EZY57HF", 184.31, 4991.1, location.Location(-0.26, 51.55),coords),
        Flight("BAW252N", 68.94, 137.16, location.Location(-0.54, 51.48),coords),
        Flight("UAL924", 67.91, -30.48, location.Location(-0.50, 51.48),coords),
    ]

    # Manually set status since you're not calling `set_flight_status()` in this demo
    flights[0].set_flight_status(Flight_Status.GROUNDED)
    flights[1].set_flight_status(Flight_Status.IN_FLIGHT)
    flights[2].set_flight_status(Flight_Status.LANDING)
    flights[3].set_flight_status(Flight_Status.LANDING)

    # Center map around Heathrow Airport (EGLL)
    map_center = [51.47, -0.45]
    m = folium.Map(location=map_center, zoom_start=10)
    # Add flights to the map
    for flight in flights:
        lat = flight.current_location.latitude
        lon = flight.current_location.longitude
        popup = (
            f"<b>{flight.call_sign}</b><br>"
            f"Altitude: {flight.altitude if flight.altitude != 'Unknown' else 'N/A'} m<br>"
            f"Speed: {flight.speed} m/s<br>"
            f"Status: {flight.status.name}"
        )
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=folium.Icon(color=get_icon_color(flight.status))
        ).add_to(m)

    # Save to HTML

    mod_path = Path(__file__).parent
    relative_path = '../flask_components/templates/flight_tracker.html'
    src_path = (mod_path / relative_path).resolve()
    m.save(src_path)
    print("Map saved as flight_tracker.html — open it in your browser.")


# Helper to determine icon color
def get_icon_color(status):
    if status == Flight_Status.IN_FLIGHT:
        return 'blue'
    elif status == Flight_Status.LANDING:
        return 'orange'
    elif status == Flight_Status.TAKING_OFF:
        return 'red'
    else:
        return 'green'


