import requests

url = "http://localhost:8000/api/v1/read-table"
files = {"file": open("test_img.png", "rb")}

response = requests.post(url, files=files)
print(response.json())