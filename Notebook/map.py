import requests

def get_current_location():
    url = "http://ip-api.com/json/"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'success':
        return {
            "latitude": data['lat'],
            "longitude": data['lon'],
            "city": data['city'],
            "region": data['regionName'],
            "country": data['country'],
            "ip": data['query']
        }
    else:
        return {"error": "Unable to get location"}

location = get_current_location()
print(location["latitude"],location["longitude"])