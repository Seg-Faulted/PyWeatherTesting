import os
import streamlit as st

import requests
import json

# Load environment variables


# User input for location
location = st.text_input("Location")

# Initialize default values
temperatureF = "NULL"
shortForecast = "NULL"
windSpeed = "NULL"  # Initialize windSpeed to NULL
windDirection = "NULL"  # Initialize windDirection to NULL
relativeHumidity = "NULL"  # Placeholder for relative humidity data

if location:
    # Split the input by commas and strip whitespace
    location_parts = [part.strip() for part in location.split(",")]

    # Assign to variables (ensure there are enough parts)
    if len(location_parts) == 3:
        City, State, Country = location_parts

        # Geoapify API call
        url = f'https://api.geoapify.com/v1/geocode/search?text={City}%2C%20{State}%2C%20{Country}&format=json&apiKey={os.getenv("d1e764a1fe174a7e99ba01f1dd3cf91a")}'
        response = requests.get(url)
        json_data = json.loads(response.text)

        # Check if results are available
        if json_data["results"]:
            latitude = json_data["results"][0]["lat"]
            longitude = json_data["results"][0]["lon"]

            # Weather.gov API call
            forecast_office_url = f'https://api.weather.gov/points/{latitude},{longitude}'
            response2 = requests.get(forecast_office_url)
            json_data2 = json.loads(response2.text)

            # Extract CWA, gridX, and gridY
            cwa = json_data2["properties"]["cwa"]
            gridX = json_data2["properties"]["gridX"]
            gridY = json_data2["properties"]["gridY"]

            # Hourly forecast API call
            url3 = f'https://api.weather.gov/gridpoints/{cwa}/{gridX},{gridY}/forecast/hourly?units=us'
            response3 = requests.get(url3)
            json_data3 = json.loads(response3.text)

            # Extract temperature, wind speed, and direction
            temperatureF = json_data3["properties"]["periods"][0].get("temperature", "NULL")
            shortForecast = json_data3["properties"]["periods"][0].get("shortForecast", "NULL")
            windSpeed = json_data3["properties"]["periods"][0].get("windSpeed", "NULL")
            windDirection = json_data3["properties"]["periods"][0].get("windDirection", "NULL")

            # Extract relative humidity
            relativeHumidity = json_data3["properties"]["periods"][0].get("relativeHumidity", {}).get("value", "NULL")

        else:
            st.warning("No results found for the specified location.")
    else:
        st.warning("Please enter the location in the format: City, State, Country")

# Streamlit metrics display
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{temperatureF} °F")
col2.metric("Wind", f"{windSpeed} {windDirection}" if windDirection != "NULL" else "NULL")
col3.metric("Humidity", f"{relativeHumidity}%" if relativeHumidity != "NULL" else "NULL")
st.divider()

# Forecast display
col1, col2 = st.columns(2)
with col1:
    st.header("Forecast")
    st.markdown(shortForecast)

with col2:
    pass
