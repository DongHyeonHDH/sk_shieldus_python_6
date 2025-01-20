from flask import Flask, render_template, request
import requests
import json, os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/recommand_hwang', methods=['GET', 'POST'])
def recommand_hwang():
    citys = [
    "Paris", "New York", "Tokyo", "London", "Rome",
    "Dubai", "Barcelona", "Istanbul", "Bangkok", "Singapore",
    "Los Angeles", "Amsterdam", "Hong Kong", "Berlin", "Sydney",
    "Venice", "Prague", "Seoul", "San Francisco", "Kyoto"
    ]
    weather_data = []
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
            "city": city,
            "temp": data["main"]["feels_like"],
            "weather": data["weather"][0]["description"], 
            "detail": link_city,
            "update_time": c_time
        }
        if w_data["temp"] > 12 and w_data["temp"] < 32:
            weather_data.append(w_data)    
        

        
    
    
    return render_template('recommand_hwang.html', weather_data = weather_data)   



if __name__ == "__main__":
    app.run(debug=True)