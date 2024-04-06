from secretos import trigger_exam_update
import requests

req = requests.post(f"http://tele2notion.eu.pythonanywhere.com/{trigger_exam_update}")

print(req)

