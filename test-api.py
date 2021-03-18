import requests

API_URL = 'http://localhost:8000/'
API_KEY = None
headers = {'UserAPI-Key': API_KEY}

#with open('main.py', 'rb') as fp:
with open('dataset/images/angular.png', 'rb') as fp:
    content = fp.read()
    print(len(content))

response = requests.post(
    f'{API_URL}/files/angular.png', headers=API_KEY, data=content
)

print(response.status_code, response.text)
