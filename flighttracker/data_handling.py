import asyncio
import time
import aiohttp
import flight
import location
from python_opensky import OpenSky, StatesResponse
from geopy.distance import geodesic


async def get_last_day_arrivals():
    airport = "EGLL"
    end = int(time.time())
    begin = end - 24*60*60
    url = "https://opensky-network.org/api/flights/arrival"
    params={
        "airport": airport, 
        "begin": begin, 
        "end": end
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                print(f"Error {response.status}: {await response.text()}")
                return None
            responses =  await response.json()

    for flight in responses:  # limit for clarity
            callsign = flight["icao24"].strip() if flight["icao24"]else "N/A"
            #speed = flight.velocity if flight.velocity else 0.0  # velocity (m/s)
            #altitude = flight.barometric_altitude if flight.barometric_altitude else 0.0  # barometric altitude (m)

            airline = callsign[:3] if callsign != "N/A" else "Unknown"
            origin  = flight["estDepartureAirport"]
            
            print(f"Callsign: {callsign}, Airline: {airline}, Origin: {origin}")
    aiohttp.ClientSession.close()
    return responses
    

async def flights_in_area(radius):
    api = OpenSky()
    states: StatesResponse = await api.get_states()

    print(f"Checking aircraft en route to Heathrow (within {radius} km)...\n")
    
    count = 0
    flights = []
    for s in states.states:
        lat = s.latitude
        lon = s.longitude
        if geodesic((lat, lon), (51.4700, -0.4543)).km <= radius:

            current_flight = flight.Flight(callsign = s.callsign or "Unknown\t",speed = s.velocity or "Unknown",altitude = s.barometric_altitude or "Unknown",location = location.Location(lon,lat))
            if s.on_ground:
                current_flight.set_flight_status(flight.Flight_Status.GROUNDED)
            elif s.vertical_rate < -1 and s.barometric_altitude < 175:
                current_flight.set_flight_status(flight.Flight_Status.LANDING)
            elif s.vertical_rate > 1 and s.barometric_altitude < 175:
                current_flight.set_flight_status(flight.Flight_Status.TAKING_OFF)
            else:
                current_flight.set_flight_status(flight.Flight_Status.IN_FLIGHT)
            flights.append(current_flight)
            
            count += 1
    api.close
    

    return flights

async def main():
   #response = await get_last_day_arrivals()
   flights = await flights_in_area(20)
   for flight in flights:
        print(flight)
        



        


if __name__ == "__main__":
    asyncio.run(main())
