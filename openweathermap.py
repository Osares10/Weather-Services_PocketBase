# Description: This script will make a request to the OpenWeatherMap API and save the data to PocketBase
import requests
import json
from datetime import datetime

# Define API endpoint and parameters
api_key = "YOUR-API-KEY" # OpenWeatherMap API key
latitude = XX.XX # Latitude of the location
longitude = XXX.XX # Longitude of the location
url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=" + api_key
pocketbase_api_url = "https://custom.domain/collections/collection_name/records" # Pocketbase API endpoint
headers = {
    "Content-Type": "application/json",
}

# Define function to get current time
def execution_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Print execution time
print(execution_time() + " - Executing script...")

# Make API request
print(execution_time() + " - Making request to OpenWeatherMap...")

response = requests.get(url)

# Check if response was successful
if response.status_code == 200:
    print(execution_time() + " - Request to OpenWeatherMap successful!")
    # Parse JSON response
    data = json.loads(response.text)

    data = json.dumps(data, indent=4)

    new_data = {
        "time": datetime.utcfromtimestamp(json.loads(data)['dt']).strftime('%Y-%m-%d %H:%M:%S.000Z'),
        "temperature": json.loads(data)['main']['temp'],
        "feels_like": json.loads(data)['main']['feels_like'],
        "pressure": json.loads(data)['main']['pressure'],
        "humidity": json.loads(data)['main']['humidity'],
        "wind_speed": json.loads(data)['wind']['speed'],
        "wind_direction": json.loads(data)['wind']['deg'],
    }

    # Make API request to PocketBase
    print(execution_time() + " - Sending data to PocketBase with date and time: " + new_data['time'])
    response = requests.post(pocketbase_api_url, headers=headers, data=json.dumps(new_data))

    if response.status_code == 200:
        print(execution_time() + " - Data sent to PocketBase successfully!")
    else:
        print(execution_time() + " - Request to PocketBase API failed! with status code: " + str(response.status_code))
else:
    print(execution_time() + " - Request to OpenWeatherMap failed! with status code: " + str(response.status_code))