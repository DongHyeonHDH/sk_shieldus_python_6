import requests
import json
 
city = "Seoul"                                #해당지역
apikey = "e2599548788383434c665766baafeb57"   #api키 (무료 키 - 송승현)
lang = "kr"                                   #언어 
 
api = f"""http://api.openweathermap.org/data/2.5/\
weather?q={city}&appid={apikey}&lang={lang}&units=metric"""
 
result = requests.get(api)
 
data = json.loads(result.text)

# 지역 : name
print(f"{data["name"]}의 날씨입니다.")
# 자세한 날씨 : weather - description
print(f"날씨는 {data['weather'][0]['description']}입니다.")
# 현재 온도 : main - temp
print(f"현재 온도는 {data["main"]["temp"]}입니다.")
# 체감 온도 : main - feels_like
print(f"하지만 체감 온도는 {data["main"]["feels_like"]}입니다.")
# 최저 기온 : main - temp_min
print(f"최저 기온은 {data["main"]["temp_min"]}입니다.")
# 최고 기온 : main - temp_max
print(f"최고 기온은 {data["main"]["temp_max"]}입니다.")
# 습도 : main - humidity
print(f"습도는 {data["main"]["humidity"]}입니다.")
# 기압 : main - pressure
print(f"기압은 {data["main"]["pressure"]}입니다.")
# 풍향 : wind - deg
print(f"풍향은 {data["wind"]["deg"]}입니다.")
# 풍속 : wind - speed
print(f"풍속은 {data["wind"]["speed"]}입니다.")