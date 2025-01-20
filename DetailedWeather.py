from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

def translate_day(day_name):
    days = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }
    return days.get(day_name, day_name)

def translate_weather(description):
    weather_conditions = {
        "clear sky": "맑음",
        "few clouds": "구름 조금",
        "scattered clouds": "흩어진 구름",
        "broken clouds": "구름 많음",
        "shower rain": "소나기",
        "rain": "비",
        "thunderstorm": "뇌우",
        "snow": "눈",
        "mist": "안개",
        "overcast clouds": "흐림"
    }
    return weather_conditions.get(description, description)

@app.route('/')
def get_weather_data():
    city = "Seoul"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    
    response = requests.get(url)
    data = response.json()
    
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    
    temp_max = round(data['main']['temp_max'], 1)
    temp_min = round(data['main']['temp_min'], 1)
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    feels_like = round(data['main']['feels_like'], 1)
    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M')
    
    today_weather = {
        "온도 요약": f"{temp_max}°C / {temp_min}°C (체감: {feels_like}°C)",
        "습도": "좋음" if humidity <= 30 else "나쁨" if humidity >= 70 else f"{humidity}%",
        "풍속": "약한 바람" if wind_speed <= 10 else "다소 강한 바람" if 10 < wind_speed <= 15 else "매우 강한 바람" if 25 < wind_speed <= 30 else f"{wind_speed} m/s",
        "일출": sunrise,
        "일몰": sunset
    }
    
    weekly_forecast = []
    current_day = datetime.utcnow()
    for i in range(8, len(forecast_data['list']), 8):  # 오늘 날짜를 제외하고 매일 데이터만 선택 (8개 간격)
        day = forecast_data['list'][i]
        date = current_day + timedelta(days=i//8)
        day_name = translate_day(date.strftime('%A'))
        weather = translate_weather(day['weather'][0]['description'])
        temp = round(day['main']['temp'], 1)
        feels_like = round(day['main']['feels_like'], 1)
        wind_speed = day['wind']['speed']
        icon = day['weather'][0]['icon']
        weekly_forecast.append({
            "요일": day_name,
            "날씨": weather,
            "온도": f"{temp}°C",
            "체감 온도": f"{feels_like}°C",
            "풍속": f"{wind_speed} m/s",
            "아이콘": icon,
            "최고 온도": f"{temp_max}°C",
            "최저 온도": f"{temp_min}°C",
            "습도": today_weather["습도"],
            "일출": today_weather["일출"],
            "일몰": today_weather["일몰"]
        })
    
    return render_template('Detailed_Weather.html', weather=today_weather, city=city, weekly_forecast=weekly_forecast)

if __name__ == "__main__":
    app.run(debug=True)