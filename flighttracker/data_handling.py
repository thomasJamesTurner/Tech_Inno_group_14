import asyncio
import time
import aiohttp
import flighttracker.flight as flight
import flighttracker.location as location
from python_opensky import OpenSky, StatesResponse
from geopy.distance import geodesic
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
from datetime import datetime, timedelta
import pytz
import sqlite3
import dotenv

def init_db(db_path="flights.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            callsign TEXT,
            speed REAL,
            altitude REAL,
            latitude REAL,
            longitude REAL,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_flight_to_db(flight_obj, db_path="flights.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flights_table (timestamp, callsign, speed, altitude, latitude, longitude, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now(),
        flight_obj.call_sign,
        flight_obj.speed,
        flight_obj.altitude,
        flight_obj.current_location.latitude,
        flight_obj.current_location.longitude,
        str(flight_obj.status)
    ))
    conn.commit()
    conn.close()

def load_flights_from_db(limit=10):
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flights_table ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()

    conn.close()
    return rows


async def get_airport_coordinates(ICAO):
    apiToken = dotenv.get_key("apikeys.env", "AIRPORT_KEY")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://airportdb.io/api/v1/airport/{ICAO}?apiToken={apiToken}") as response:
            if response.status == 200:
                data = await response.json()
                return (data['latitude_deg'], data['longitude_deg'])
    return None

async def get_airport_weather(ICAO):
    # Using coordinates to get weather site number
    coords = await get_airport_coordinates(ICAO)
    if not coords:
        return None
    
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    url = "https://api.open-meteo.com/v1/forecast"
    now = datetime.now(pytz.timezone("GMT"))
    end_time = now + timedelta(hours=36)

    params = {
        "latitude": coords[0],
        "longitude": coords[1],
        "hourly": "temperature_2m,weathercode",
        "timezone": "GMT",
        "start_date": now.strftime("%Y-%m-%d"),
        "end_date": end_time.strftime("%Y-%m-%d")
    }
    
    responses = openmeteo.weather_api(url, params=params)
    data = responses[0]
    hourly = data.Hourly()
    
    # Convert the time data to ISO format strings
    time_array = pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )
    
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy().tolist()
    hourly_weathercode = hourly.Variables(1).ValuesAsNumpy().tolist()
    

    weather_data = []
    for i in range(len(time_array)):
        if now <= time_array[i].to_pydatetime() <= end_time:
            weather_data.append({
                "time": time_array[i].isoformat(),
                "temperature": float(hourly_temperature_2m[i]),  
                "weathercode": int(hourly_weathercode[i])        
            })
    
    return weather_data

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
    return responses
    

async def flights_in_area(ICAO,radius):
    api = OpenSky()
    states: StatesResponse = await api.get_states()

    print(f"Checking aircraft en route to airport (within {radius} km)...\n")
    
    count = 0
    flights = []
    coords = get_airport_coordinates(ICAO)
    print(coords)
    for s in states.states:
        lat = s.latitude
        lon = s.longitude
        if geodesic((lat, lon), coords).km <= radius:

            current_flight = flight.Flight(callsign = s.callsign or "Unknown",speed = s.velocity or "Unknown",altitude = s.barometric_altitude or "Unknown",location = location.Location(lon,lat), airport_coords=coords)
            if s.barometric_altitude != None and s.vertical_rate != None:
                if s.on_ground:
                    current_flight.set_flight_status(flight.Flight_Status.GROUNDED)
                elif s.vertical_rate < -1 and s.barometric_altitude < 175:
                    current_flight.set_flight_status(flight.Flight_Status.LANDING)
                elif s.vertical_rate > 1 and s.barometric_altitude < 175:
                    current_flight.set_flight_status(flight.Flight_Status.TAKING_OFF)
                else:
                    current_flight.set_flight_status(flight.Flight_Status.IN_FLIGHT)
            else:
                    current_flight.set_flight_status(flight.Flight_Status.IN_FLIGHT)
            flights.append(current_flight)
            
            count += 1
    await api.close()
    

    return flights

async def main():
    print(get_airport_weather("EGLL"))
    #init_db()  # Create the database and table
    #flights = await flights_in_area("EGLL", 20)
    #for f in flights:
    #    save_flight_to_db(f)
    #    print(f)

        



        


if __name__ == "__main__":
    asyncio.run(main())