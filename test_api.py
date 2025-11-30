import requests

url = "http://localhost:8000/api/v1/read-table"
files = {"file": open("test_img2.png", "rb")}

response = requests.post(url, files=files, params={"score_error_exceptions": "true"})
print(response.json())