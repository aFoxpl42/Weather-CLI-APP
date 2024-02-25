import requests
import json
from secret import *

# In order to make this work you need to provide your own API KEY.

while True:
    print("Welcome to my forecast application. Press 'q' at any time to leave.") 
    
    city = input("Which city are you interested in? ").title()
    
    if city.lower() == 'q':
        break
    
    response_API = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=10&aqi=yes&alerts=yes')
    
    if response_API.status_code == 400:
        print("You have provided invalid location. Please try again.")
        break
    
    data = response_API.text
    
    parse_json = json.loads(data)
    
    print("--------------------------------------------------------")
    print(f"Introduction data for weather in: {parse_json['location']['name']}, {parse_json['location']['country']}")
    print("--------------------------------------------------------")
    print(f"Last data update at: {parse_json['current']['last_updated']}")
    print("--------------------------------------------------------")
    print(f"It is currently {parse_json['current']['condition']['text'].lower()}")
    print("--------------------------------------------------------")


    def temperature_current():
        temp_data = parse_json['current']
        if temp_data['temp_c'] == temp_data['feelslike_c']:
            print(f"Temperature in C: {temp_data['temp_c']}\nAnd it feels like it.")
        else:
            print(f"Temperature in C: {temp_data['temp_c']}\nBut it feels more like {temp_data['feelslike_c']}")


    def wind_current():
        wind_data = parse_json['current']
        print(f"Wind speed: {wind_data['wind_kph']}km/h")
        print(f"Wind direction: {wind_data['wind_dir']}")
        
        
    def forecast(day):
        
        data = parse_json['forecast']['forecastday'][day]['day'] # [x] is day; 0 is today etc.
        print(f"Forecast for {parse_json['forecast']['forecastday'][day]['date']}")
        print("--------------------------------------------------------")
        print(f"Maximum temperature: {data['maxtemp_c']}")
        print(f"Minimum temperature: {data['mintemp_c']}")
        print(f"Average temperature: {data['avgtemp_c']}")
        print("--------------------------------------------------------")
        print(f"It will be {data['condition']['text'].lower()}")
        print(f"Maximum wind speed in km/h: {data['maxwind_kph']}")
        print("--------------------------------------------------------")
        if data['daily_will_it_rain'] == 1:
            print(f"It will rain ({data['daily_chance_of_rain']}% chance)")
        else:
            print(f"No rain.")
        if data['daily_will_it_snow'] == 1:
            print(f"It will snow ({data['daily_chance_of_snow']}% chance)")
        else:
            print(f"No snow.")
        print("--------------------------------------------------------")


    show_temperature_current = input(f"Are you interested in current temperature in {city.title()}? (y/n) ").lower()
    if show_temperature_current == 'q':
        break
    elif show_temperature_current == 'y':
        temperature_current()
    elif show_temperature_current == 'n':
        pass
    
    show_wind_current = input(f"Are you interested in current wind state in {city} (y/n) ").lower()
    if show_wind_current == 'q':
        break
    elif show_wind_current == 'y':
        wind_current()
    elif show_wind_current == 'n':
        pass
    
    show_forecast = input(f"Are you interested in forecast for {city}? (y/n) ").lower()
    if show_forecast == 'q':
        break
    elif show_forecast == 'n':
        break
    elif show_forecast == 'y':
        day_input = input("When? (enter a number; 0 is today, 1 is tomorrow etc.)(max 9 days ahead) ")
        if day_input == 'q':
            break
        elif day_input.isdigit() == False:
            print("Invalid input. Please try again.")
            day_input = input("When? (enter a number; 0 is today, 1 is tomorrow etc.)(max 9 days ahead)    ")            
        elif day_input.isdigit() and int(day_input) <= 9:
            forecast(int(day_input))