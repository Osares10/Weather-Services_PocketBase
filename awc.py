# Description: Fetches METAR data from Aviation Weather Center API and posts it to PocketBase API

# Import libraries
import requests
import csv
import json
from datetime import datetime

# Define constants
API_URL = "https://www.aviationweather.gov/adds/dataserver_current/httpparam" # Aviation Weather Center API URL
POCKETBASE_API_URL = "https://custom.domain/api/collections/collection_name/records" # PocketBase API URL

# Define variables
data_type = "metars"
airport_code = "XXXX" # Airport code
hours_before_now = "24" # Number of hours before now to fetch data for
output_format = "csv"

# Define function to get current time
def execution_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Define function to fetch CSV data
def fetch_csv_data(api_url, parameters):
    print(execution_time() + " - Making request to Aviation Weather Center...")
    # Make the API request
    response = requests.get(api_url, params=parameters)
    # Check for successful request
    if response.status_code == 200:
        # Decode the CSV content
        content = response.content.decode("utf-8")
        # Parse the CSV data and return it
        csv_data = list(csv.reader(content.splitlines(), delimiter=","))
        return csv_data
    else:
        print(execution_time() + " - Request to Aviation Weather Center failed! with status code: " + str(response.status_code))

# Set up the API request parameters
parameters = {
    "dataSource": data_type,
    "requestType": "retrieve",
    "format": output_format,
    "stationString": airport_code,
    "hoursBeforeNow": hours_before_now,
}

# Print execution time
print(execution_time() + " - Executing script...")

# Call the function to fetch the CSV data
csv_data = fetch_csv_data(API_URL, parameters)

# Check if there are results in the CSV data
if len(csv_data) <= 6:
    print(execution_time() + " - No results found in CSV data received from Aviation Weather Center")
else:
    print(execution_time() + " - CSV data received from Aviation Weather Center successfully!")
    # Parse the remaining rows of the CSV data and convert to JSON
    print(execution_time() + " - Parsing CSV data and converting it to JSON...")
    for row in csv_data[6:]: # Skip the first 6 rows
        # Get the headers from the first row of the CSV data
        headers = csv_data[5]
        # Create a dictionary with the desired keys and values
        data = {
            "raw_text": row[headers.index("raw_text")],
            "station_id": airport_code,
            "observation_time": datetime.strptime(row[headers.index("observation_time")], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S.000Z"),
            "temp_c": float(row[headers.index("temp_c")]),
            "dewpoint_c": float(row[headers.index("dewpoint_c")]) if row[headers.index("dewpoint_c")] else 99, # Set to 99 if dewpoint_c is empty
            "wind_dir_degrees": int(row[headers.index("wind_dir_degrees")]) if row[headers.index("wind_dir_degrees")] else 0,
            "wind_speed_kt": int(row[headers.index("wind_speed_kt")]) if row[headers.index("wind_speed_kt")] else 0,
            "altim_in_hg": float(row[headers.index("altim_in_hg")]),
            "corrected": bool(row[headers.index("corrected")]),
            "precip_in": float(row[headers.index("precip_in")]) if row[headers.index("precip_in")] else 0,
            "metar_type": row[headers.index("metar_type")],
        }

        # Set up the headers for the POST request
        headers = {'Content-Type': 'application/json'}

        # Make the POST request to PocketBase API
        print(execution_time() + " - Sending data to PocketBase with date and time: " + data["observation_time"])
        response = requests.post(POCKETBASE_API_URL, data=json.dumps(data), headers=headers)

        # Check for successful request
        if response.status_code == 200:
            print(execution_time() + " - Data sent to PocketBase successfully!")
        else:
            print(execution_time() + " - Request to PocketBase failed! with status code: " + str(response.status_code))