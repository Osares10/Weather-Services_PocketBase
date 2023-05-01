# Description: This script is used to get the weather data from the OpenMeteo API and send it to Pocketbase

# Import libraries
import requests
import json
from datetime import datetime
from datetime import date
from datetime import timedelta

# Define API endpoint and parameters
url = "https://api.open-meteo.com/v1/forecast" # OpenMeteo API endpoint
pocketbase_api_url = "https://w.arias.pw/api/collections/open_meteo/records" # Pocketbase API endpoint
headers = {
    "Content-Type": "application/json",
}

# Get previous day
previous_day = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

params = {
    "latitude": XX.XX, # Latitude of the location
    "longitude": XXX.XX, # Longitude of the location
    "hourly": "temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,rain,pressure_msl,surface_pressure,visibility,windspeed_10m,windspeed_80m,windspeed_120m,windspeed_180m,winddirection_10m,winddirection_80m,winddirection_120m,winddirection_180m,temperature_80m,temperature_120m,temperature_180m,uv_index",
    "windspeed_unit": "kn", # Unit of the wind speed
    "precipitation_unit": "inch", # Unit of the precipitation
    "forecast_days": 1, 
    "start_date": previous_day, # Start date of the forecast
    "end_date": previous_day # End date of the forecast, for one day, use the same date as start_date
}

# Define function to get current time
def execution_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Print execution time
print(execution_time() + " - Executing script...")

# Make API request
print(execution_time() + " - Making request to open-meteo...")
response = requests.get(url, params=params)

# Check if response was successful
if response.status_code == 200:
    # Print response
    print(execution_time() + " - Response from open-meteo was successful!")

    # Parse JSON response
    data = json.loads(response.text)

    # Structure data
    data = json.dumps(data, indent=4)

    # Send data to Pocketbase API one hour at a time
    for hour in range(0, len(json.loads(data)['hourly']['time'])):
        new_data = {
            "time": datetime.strptime(json.loads(data)['hourly']['time'][hour], "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:00.000Z"),
            "temperature_2m": json.loads(data)['hourly']['temperature_2m'][hour],
            "relativehumidity_2m": json.loads(data)['hourly']['relativehumidity_2m'][hour],
            "dewpoint_2m": json.loads(data)['hourly']['dewpoint_2m'][hour],
            "apparent_temperature": json.loads(data)['hourly']['apparent_temperature'][hour],
            "rain": json.loads(data)['hourly']['rain'][hour],
            "pressure_msl": json.loads(data)['hourly']['pressure_msl'][hour],
            "surface_pressure": json.loads(data)['hourly']['surface_pressure'][hour],
            "windspeed_10m": json.loads(data)['hourly']['windspeed_10m'][hour],
            "windspeed_80m": json.loads(data)['hourly']['windspeed_80m'][hour],
            "windspeed_120m": json.loads(data)['hourly']['windspeed_120m'][hour],
            "windspeed_180m": json.loads(data)['hourly']['windspeed_180m'][hour],
            "winddirection_10m": json.loads(data)['hourly']['winddirection_10m'][hour],
            "winddirection_80m": json.loads(data)['hourly']['winddirection_80m'][hour],
            "winddirection_120m": json.loads(data)['hourly']['winddirection_120m'][hour],
            "winddirection_180m": json.loads(data)['hourly']['winddirection_180m'][hour],
            "temperature_80m": json.loads(data)['hourly']['temperature_80m'][hour],
            "temperature_120m": json.loads(data)['hourly']['temperature_120m'][hour],
            "temperature_180m": json.loads(data)['hourly']['temperature_180m'][hour],
            "uv_index": json.loads(data)['hourly']['uv_index'][hour]
        }
        # Send data to Pocketbase API
        print(execution_time() + " - Sending data to PocketBase with date and time: " + new_data["time"])
        
        response = requests.post(pocketbase_api_url, headers=headers, data=json.dumps(new_data))

        # Check if response was successful
        if response.status_code == 200:
            print(execution_time() + " - Request to Pocketbase was successful!")
        else:
            print(execution_time() + " - Request to Pocketbase failed! with status code: " + str(response.status_code))
else:
    print(execution_time() + " - Request to open-meteo failed! with status code: " + str(response.status_code))