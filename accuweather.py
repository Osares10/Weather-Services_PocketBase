import requests
import json
from datetime import datetime

# Define API endpoint and parameters
location_key = "YOUR-LOCATION-KEY" # Location key
api_key = "YOUR-API-KEY" # AccuWeather API key
pocketbase_api_url = "https://custom.domain/api/collections/collection_name/records" # Pocketbase API endpoint

# Define headers
headers = {
    "Content-Type": "application/json",
}

# Define function to get current time
def execution_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Print execution time
print(execution_time() + " - Executing script...")

# Make API request
print(execution_time() + " - Making request to AccuWeather...")
response = requests.get("http://dataservice.accuweather.com/currentconditions/v1/" + location_key + "/historical/24?apikey=" + api_key + "&language=en-us&details=true&metric=true")
data = json.loads(response.text)
data = json.dumps(data, indent=4)

# Check if response was successful
if response.status_code == 200:
    print(execution_time() + " - Request to AccuWeather successful!")
    # Parse JSON response
    for i in range(0, len(json.loads(data))):
        new_data = {
            "time": datetime.utcfromtimestamp(json.loads(data)[i]['EpochTime']).strftime('%Y-%m-%d %H:%M:%S.000Z'),
            "temperature": json.loads(data)[i]['Temperature']['Metric']['Value'],
            "realFeelTemperature": json.loads(data)[i]['RealFeelTemperature']['Metric']['Value'],
            "realFeelTemperatureShade": json.loads(data)[i]['RealFeelTemperatureShade']['Metric']['Value'],
            "relativeHumidity": json.loads(data)[i]['RelativeHumidity'],
            "indoorRelativeHumidity": json.loads(data)[i]['IndoorRelativeHumidity'],
            "dewPoint": json.loads(data)[i]['DewPoint']['Metric']['Value'],
            "windDirection": json.loads(data)[i]['Wind']['Direction']['Degrees'],
            "windSpeed": json.loads(data)[i]['Wind']['Speed']['Metric']['Value'],
            "uvIndex": json.loads(data)[i]['UVIndex'],
            "visibility": json.loads(data)[i]['Visibility']['Imperial']['Value'],
            "pressure": json.loads(data)[i]['Pressure']['Imperial']['Value'],
            "apparentTemperature": json.loads(data)[i]['ApparentTemperature']['Metric']['Value'],
            "precipitation": json.loads(data)[i]['Precip1hr']['Metric']['Value'],
        }
        # Send data to PocketBase API
        print(execution_time() + " - Sending data to PocketBase with date and time: " + new_data['time'])

        response = requests.post(pocketbase_api_url, headers=headers, data=json.dumps(new_data))

        # Check if response was successful
        if response.status_code == 200:
            print(execution_time() + " - Data sent to PocketBase successfully!")
        else:
            print(execution_time() + " - Request to PocketBase failed! with status code: " + str(response.status_code))

else:
    print(execution_time() + "Request to AccuWeather failed! with response code: " + str(response.status_code))