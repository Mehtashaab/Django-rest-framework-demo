import requests

endpoints ="http://localhost:8000/car/list"

getresponse = requests.get(endpoints).json()

#print(getresponse.status_code)
print(getresponse)