import requests
from flask import Flask, render_template

# Flask 애플리케이션 생성
app = Flask(__name__)

# API KEY와 도시 설정
API_KEY = '9cae5455896ac60736d3819e002c11af'

# 날씨 데이터를 받아오는 함수
def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    res = requests.get(url, params=params)
    data = res.json()

    # 데이터 초기화
    weather_data = {
        'humidity': None,
        'temp_min': None,
        'temp_max': None,
        'pressure': None,
        'wind_speed': None,
        'wind_deg': None
    }

    # 데이터 추출
    for key, value in data.items():
        if key == 'main':
            weather_data['humidity'] = value['humidity']
            weather_data['temp_min'] = value['temp_min']
            weather_data['temp_max'] = value['temp_max']
            weather_data['pressure'] = value['pressure']

        elif key == 'wind':
            weather_data['wind_speed'] = value['speed']
            wind_deg = value['deg']

            if 0 <= wind_deg < 22.5 or 337.5 <= wind_deg <= 360:
                weather_data['wind_deg'] = f"{wind_deg}° 북"
            elif 22.5 <= wind_deg < 67.5:
                weather_data['wind_deg'] = f"{wind_deg}° 북동"
            elif 67.5 <= wind_deg < 112.5:
                weather_data['wind_deg'] = f"{wind_deg}° 동"
            elif 112.5 <= wind_deg < 157.5:
                weather_data['wind_deg'] = f"{wind_deg}° 남동"
            elif 157.5 <= wind_deg < 202.5:
                weather_data['wind_deg'] = f"{wind_deg}° 남"
            elif 202.5 <= wind_deg < 247.5:
                weather_data['wind_deg'] = f"{wind_deg}° 남서"
            elif 247.5 <= wind_deg < 292.5:
                weather_data['wind_deg'] = f"{wind_deg}° 서"
            elif 292.5 <= wind_deg < 337.5:
                weather_data['wind_deg'] = f"{wind_deg}° 북서"
    return weather_data

# 웹 페이지를 렌더링하는 route
@app.route('/')
def index():
    city= 'Tokyo'
    weather_data = get_weather_data(city)
    return render_template('detail_weather.html', city= city, weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
