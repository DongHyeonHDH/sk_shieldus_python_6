import requests
import json
import pandas as pd

# API 요청 정보
city = "Seoul, london, tokyo, new york, paris, sydney"                                # 해당 지역
apikey = "e2599548788383434c665766baafeb57"   # API 키
lang = "kr"                                   # 언어
api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"

# API 요청
result = requests.get(api)
data = json.loads(result.text)  # JSON 데이터를 파싱

# 필요한 데이터 추출
weather_data = {
    "도시": city,
    "날씨": data["weather"][0]["description"],
    "온도(°C)": data["main"]["temp"],
    "체감온도(°C)": data["main"]["feels_like"],
    "최저온도(°C)": data["main"]["temp_min"],
    "최고온도(°C)": data["main"]["temp_max"],
    "습도(%)": data["main"]["humidity"],
    "풍속(m/s)": data["wind"]["speed"]
}

# 데이터프레임 생성
df = pd.DataFrame([weather_data])

# Excel 파일로 저장
file_name = "weather_data.xlsx"
df.to_excel(file_name, index=False)

print(f"날씨 정보가 '{file_name}' 파일로 저장되었습니다.")