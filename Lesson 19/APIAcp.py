import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 27.7172,
    "longitude": 85.3240,
    "current_weather": True
}

response = requests.get(url, params=params)

if response.status_code == 200:
    weather_data = response.json()
    current_weather = weather_data["current_weather"]
    
    temperature = current_weather["temperature"]
    windspeed = current_weather["windspeed"]
    weather_code = current_weather["weathercode"]

    print("🌤 Current Weather in Kathmandu 🌤")
    print(f"Temperature: {temperature}°C")
    print(f"Wind Speed: {windspeed} km/h")
    print(f"Weather Code: {weather_code}")
else:
    print(f"Error fetching data: {response.status_code}")
