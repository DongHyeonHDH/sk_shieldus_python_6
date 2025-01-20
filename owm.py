import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

weather_translation = {
    "clear sky": "맑은 하늘",
    "few clouds": "구름 조금",
    "scattered clouds": "흩어진 구름",
    "broken clouds": "짙은 구름",
    "shower rain": "소나기",
    "rain": "비",
    "thunderstorm": "뇌우",
    "snow": "눈",
    "mist": "안개",
    "fog": "안개",  
    "overcast clouds": "흐림" 
}


city_names_kor = ["서울", "도쿄", "워싱턴", "모스크바", "파리"]
weather_data = []

for city_name_kor in city_names_kor:
    params = {
        "q": city_name_kor, 
        "appid": API_KEY,   
        "units": "metric",  
        "lang": "kr"        
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        current_temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_eng = data["weather"][0]["description"] 

        weather_kor = weather_translation.get(weather_eng, weather_eng)

        weather_data.append({
            "city_name_kor": city_name_kor,
            "current_temp": current_temp,
            "feels_like": feels_like,
            "weather_kor": weather_kor
        })

weather_data.sort(key=lambda x: x["feels_like"], reverse=True)

if weather_data:
    for city in weather_data:
        print(f"도시: {city['city_name_kor']}")
        print(f"현재 온도: {city['current_temp']} °C")
        print(f"체감 온도: {city['feels_like']} °C")
        print(f"날씨: {city['weather_kor']}")