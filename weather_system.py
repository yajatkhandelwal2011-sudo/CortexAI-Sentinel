import requests

API_KEY = "98306713b1e335516f4a9c5036cdce39"

def get_weather_alert(city):

    try:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        data = response.json()

        weather = data["weather"][0]["main"]

        temp = data["main"]["temp"]

        if weather.lower() in ["storm", "thunderstorm", "tornado"]:

            risk = "🔴 HIGH RISK"

        elif weather.lower() in ["rain", "drizzle"]:

            risk = "🟠 MEDIUM RISK"

        else:

            risk = "🟢 LOW RISK"

        return {
            "weather": weather,
            "temp": temp,
            "risk": risk
        }

    except Exception as e:

        return {
            "weather": "Unknown",
            "temp": "N/A",
            "risk": f"Error: {e}"
        }
