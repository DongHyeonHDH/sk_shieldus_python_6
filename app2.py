from flask import Flask, render_template, request, send_file
import requests
import json, os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from openpyxl import Workbook
from datetime import datetime 
app = Flask(__name__)

@app.route('/download_xlsx', methods=['GET', 'POST'])
def download_xlsx():
    print('날씨정보 다운로드')
    cities = request.form.getlist('city[]')
    temps = request.form.getlist('temp[]')
    weathers = request.form.getlist('weather[]')

    wb = Workbook()
    ws = wb.active
    ws.title = '추천 여행지 날씨 정보'

    ws.append(['도시', '온도', '날씨'])

    for i in range(len(cities)):
        ws.append([cities[i], temps[i], weathers[i]])
    today = datetime.now().strftime('%Y%m%d')
    wb.save(f'[{today}]excel.xlsx')

    return send_file(f'[{today}]excel.xlsx', as_attachment=True)

@app.route('/recommand_hwang', methods=['GET', 'POST'])
def recommand_hwang():
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
    weather_data = []
    cnt = 0
    for city in citys:     
        apikey = 'f14638e80f750690b27c459de0db1173'                             # 해당 지역
        # apikey = os.getenv("API_KEY")    # API 키
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
            "update_time": c_time
        }

        cnt += 1
        if w_data["temp"] > 12 and w_data["temp"] < 32:
            weather_data.append(w_data)    



    return render_template('recommand_hwang.html', weather_data = weather_data)   

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)