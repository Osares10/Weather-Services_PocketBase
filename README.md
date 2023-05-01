# Weather-Services_PocketBase
Get, receive and send data from various weather services such as Accuweather, AWC, open-meteo and openweathermap

Project developed in python, the documentation will not be very extensive, but it will be enough to understand the operation of the code, if you have basic knowledge of the technologies used it should be very easy to understand.

## References
- [Accuweather API](https://developer.accuweather.com/apis)
- [Aviation Weather Center](https://www.aviationweather.gov/dataserver)
- [Open-Meteo](https://open-meteo.com/en/docs)
- [OpenWeatherMap](https://openweathermap.org/api)

## Ubication, credentials and keys

`accuweather.py`
```py
location_key = "YOUR-LOCATION-KEY" # Location key
api_key = "YOUR-API-KEY" # AccuWeather API key
pocketbase_api_url = "https://custom.domain/api/collections/collection_name/records" # Pocketbase API endpoint
```

`awc.py`
```py
airport_code = "XXXX" # Airport code
```

`open-meteo.py`
```py
params = {
    "latitude": XX.XX, # Latitude of the location
    "longitude": XXX.XX, # Longitude of the location
    ...
}
```

`openweathermap.py`
```py
api_key = "YOUR-API-KEY" # OpenWeatherMap API key
latitude = XX.XX # Latitude of the location
longitude = XXX.XX # Longitude of the location
```

```py
pocketbase_api_url = "https://custom.domain/collections/collection_name/records" # Pocketbase API endpoint
```

**Note:** The integration with AWC doesn't allow to save multiple data with the same name yet, so if you requiere it, you must change the name of the data in the code.