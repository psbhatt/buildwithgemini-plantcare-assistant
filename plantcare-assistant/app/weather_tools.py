import json
import urllib.parse
import urllib.request
from typing import Any, Dict

def get_local_plant_climate(city: str) -> Dict[str, Any]:
    """Fetch live meteorological data (temperature, relative humidity, sunshine) for a city via Open-Meteo.
    Use this to give personalized plant care advice based on real ambient humidity and weather.

    Args:
        city: City or location name (e.g., 'San Francisco', 'New York', 'London').

    Returns:
        A dictionary with temperature, humidity percentage, weather condition, and plant-care recommendations.
    """
    try:
        # 1. Geocode city name to lat/lon
        encoded_city = urllib.parse.quote(city.strip())
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en&format=json"
        geo_req = urllib.request.Request(geo_url, headers={"User-Agent": "FloraPlantCare/1.0"})
        with urllib.request.urlopen(geo_req, timeout=5) as resp:
            geo_data = json.loads(resp.read().decode())
        
        results = geo_data.get("results")
        if not results:
            return {"error": f"Could not find coordinates for location: {city}"}
        
        loc = results[0]
        lat, lon = loc["latitude"], loc["longitude"]
        city_name = loc.get("name", city)
        country = loc.get("country", "")

        # 2. Fetch current weather and relative humidity
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,is_day"
            f"&timezone=auto"
        )
        weather_req = urllib.request.Request(weather_url, headers={"User-Agent": "FloraPlantCare/1.0"})
        with urllib.request.urlopen(weather_req, timeout=5) as resp:
            weather_data = json.loads(resp.read().decode())
        
        current = weather_data.get("current", {})
        temp_c = current.get("temperature_2m")
        temp_f = round((temp_c * 9/5) + 32, 1) if temp_c is not None else None
        humidity = current.get("relative_humidity_2m")

        # Botanical humidity interpretation
        if humidity is not None:
            if humidity < 35:
                humidity_status = "Very dry (low humidity). Tropical plants like Ferns, Calatheas, and Monsteras will benefit from misting or a pebble tray."
            elif 35 <= humidity <= 60:
                humidity_status = "Moderate humidity. Ideal for most common houseplants."
            else:
                humidity_status = "High humidity. Tropical plants thrive; ensure good ventilation to prevent fungal issues."
        else:
            humidity_status = "Humidity data unavailable."

        return {
            "city": city_name,
            "country": country,
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "relative_humidity_percent": humidity,
            "humidity_guidance": humidity_status
        }
    except Exception as e:
        return {"error": f"Failed to fetch weather data for {city}: {str(e)}"}
