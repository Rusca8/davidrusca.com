from secretos import trigger_weather_check
import requests

req = requests.post(f"http://tele2notion.eu.pythonanywhere.com/{trigger_weather_check}")

print(req)

