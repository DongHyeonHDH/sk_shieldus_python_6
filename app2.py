from flask import Flask, render_template, request, send_file
import requests
import json, os
import pandas as pd
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from openpyxl import Workbook

load_dotenv()
apikey = os.getenv("API_KEY")
app = Flask(__name__)

citys = [
    "Paris", "New York", "Tokyo", "London", "Rome",
    "Dubai", "Barcelona", "Istanbul", "Bangkok", "Singapore",
    "Los Angeles", "Amsterdam", "Hong Kong", "Berlin", "Sydney",
    "Venice", "Prague", "Seoul", "San Francisco", "Kyoto"
    ]
citys_kor = [
    "파리", "뉴욕", "도쿄", "런던", "로마",
    "두바이", "바르셀로나", "이스탄불", "방콕", "싱가포르",
    "로스앤젤레스", "암스테르담", "홍콩", "베를린", "시드니",
    "베네치아", "프라하", "서울", "샌프란시스코", "교토"
    ]

@app.route('/download_xlsx', methods=['POST'])
def download_xlsx():
    # 요청 URL 확인 
    request_url = request.referrer
    print(f'날씨정보 다운로드 요청URL : {request_url}')
    today = datetime.now().strftime('%Y%m%d')

    wb = Workbook()
    ws = wb.active
    save_name = ''
    if request_url[22:] == 'recommand_hwang':
        ws.title = '추천 여행지 날씨 정보'
        save_name = f'[{today}]추천_여행지.xlsx'
    elif request_url[22:] == 'cold_trip_cities':
        ws.title = '추운 여행지 날씨 정보'
        save_name = f'[{today}]추운_여행지.xlsx'
    elif request_url[22:] == 'hot_trip_cities':
        ws.title = '따듯한 여행지 날씨 정보'
        save_name = f'[{today}]따듯한_여행지.xlsx'
    ws.append(['도시', '온도', '날씨'])

    cities = request.form.getlist('city[]')
    temps = request.form.getlist('temp[]')
    weathers = request.form.getlist('weather[]')
    
    for i in range(len(cities)):
        ws.append([cities[i], temps[i], weathers[i]])
    wb.save(save_name)

    return send_file(save_name, as_attachment=True)

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

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

@app.route('/recommand_hwang', methods=['GET'])
def recommand_hwang():
    weather_data = []
    cnt = 0
    for city in citys:
        lang = "kr"       
        api =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"

        # API 요청
        result = requests.get(api)
        data = json.loads(result.text) 
        link_city = f"recommand_{city}.html"
        
        c_time = datetime.now().strftime("%Y-%m-%d")        

        # 필요한 데이터 추출     
        w_data = {
            "city": citys_kor[cnt],
            "temp": data["main"]["feels_like"],
            "weather": data["weather"][0]["description"], 
            "detail": link_city,
            "update_time": c_time,
            "city2": citys[cnt]
        }

        cnt += 1
        if w_data["temp"] > 12 and w_data["temp"] < 29:
            weather_data.append(w_data)    

    if len(weather_data) == 0:
        return render_template('no_recommand.html')
    
    return render_template('recommand_hwang.html', weather_data = weather_data)   

@app.route('/cold_trip_cities', methods=['GET', 'POST'])
def row():
    weather_data = []
    cnt = 0
    for city in citys:     
        lang = "kr"       
        api =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
        # API 요청
        result = requests.get(api)
        data = json.loads(result.text) 
        link_city = f"recommand_{city}.html"
        
        c_time = datetime.now().strftime("%Y-%m-%d")        

        # 필요한 데이터 추출     
        w_data = {
            "city": citys_kor[cnt],
            "temp": data["main"]["feels_like"],
            "weather": data["weather"][0]["description"], 
            "detail": link_city,
            "update_time": c_time,
            "city2": citys[cnt]
        }

        cnt += 1
        if cnt == 6:
            break
        if w_data["temp"] < 13:
            weather_data.append(w_data)

        if len(weather_data) == 0:
            return render_template('no_recommand.html')

    return render_template('cold_trip_cities.html', weather_data=weather_data)

@app.route('/hot_trip_cities', methods=['GET'])
def hi():
    weather_data = []
    cnt = 0
    for city in citys:     
        lang = "kr"       
        api =  f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
        # API 요청
        result = requests.get(api)
        data = json.loads(result.text) 
        link_city = f"recommand_{city}.html"
        
        c_time = datetime.now().strftime("%Y-%m-%d")        

        # 필요한 데이터 추출     
        w_data = {
            "city": citys_kor[cnt],
            "temp": data["main"]["feels_like"],
            "weather": data["weather"][0]["description"], 
            "detail": link_city,
            "update_time": c_time,
            "city2": citys[cnt]
        }

        cnt += 1
        if cnt == 6:
            break
        if w_data["temp"] < 29:
            weather_data.append(w_data)
        
        if len(weather_data) == 0:
            return render_template('no_recommand.html')
    
    if request.method == 'POST':
        wb = Workbook()
        ws = wb.active
        ws.title = '더운 여행지 날씨 정보'
        today = datetime.now().strftime('%Y%m%d')
        save_name = f'[{today}]더운_여행지.xlsx'
        ws.append(['도시', '온도', '날씨'])

        for data in weather_data:
            ws.append([data['city'], data['temp'], data['weather']])
        wb.save(save_name)

        return send_file(save_name, as_attachment=True)
    
    return render_template('hot_trip_cities.html', weather_data = weather_data)

@app.route('/detail_weather', methods=['GET'])
def get_weather_data():
    city = request.args.get('city')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric'
    
    response = requests.get(url)
    data = response.json()
    
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    
    temp_max = round(data['main']['temp_max'], 1)
    temp_min = round(data['main']['temp_min'], 1)
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    feels_like = round(data['main']['feels_like'], 1)
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=timezone.utc).strftime('%H:%M')
    sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=timezone.utc).strftime('%H:%M')
    
    today_weather = {
        "온도 요약": f"{temp_max}°C / {temp_min}°C (체감: {feels_like}°C)",
        "습도": "좋음" if humidity <= 30 else "나쁨" if humidity >= 70 else f"{humidity}%",
        "풍속": "약한 바람" if wind_speed <= 10 else "다소 강한 바람" if 10 < wind_speed <= 15 else "매우 강한 바람" if 25 < wind_speed <= 30 else f"{wind_speed} m/s",
        "일출": sunrise,
        "일몰": sunset
    }
    
    weekly_forecast = []
    current_day = datetime.now(timezone.utc)
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
            "풍속": "약한 바람" if wind_speed <= 10 else "다소 강한 바람" if 10 < wind_speed <= 15 else "매우 강한 바람" if 25 < wind_speed <= 30 else f"{wind_speed} m/s",
            "아이콘": icon,
            "최고 온도": f"{temp_max}°C",
            "최저 온도": f"{temp_min}°C",
            "습도": today_weather["습도"],
            "일출": today_weather["일출"],
            "일몰": today_weather["일몰"]
        })
    if city in citys:
        city_kor = citys_kor[citys.index(city)]
    else:
        city_kor = city
    
    return render_template('Detailed_Weather.html', weather=today_weather, city=city_kor, weekly_forecast=weekly_forecast)

if __name__ == '__main__':
    app.run(debug=True)