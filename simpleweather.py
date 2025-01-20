from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# OpenWeatherMap API 설정
API_KEY = "46b55a9f61cc588200575a3dda8e3069"
CITY = "Seoul"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY},kr&appid={API_KEY}&units=metric"

# 라우트 정의
@app.route("/")
def home():
    # OpenWeatherMap API 호출
    response = requests.get(URL)
    if response.status_code == 200:
        weather_data = response.json()
        
        # 현재 날짜
        now = datetime.now()
        current_date = f"{now.month}월 {now.day}일"
        
        # 날씨 정보 추출
        weather_info = {
            "date": current_date,
            "current_temp": weather_data["main"]["temp"],
            "low_temp": weather_data["main"]["temp_min"],
            "high_temp": weather_data["main"]["temp_max"],
            "icon_url": f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}.png",
            "description": weather_data["weather"][0]["description"],
            "region": weather_data["name"],  # 지역 이름 추가
        }
        return render_template("simpleweather.html", weather=weather_info)
    else:
        return f"OpenWeatherMap API 호출 실패: {response.status_code}"

if __name__ == "__main__":
    app.run(debug=True)