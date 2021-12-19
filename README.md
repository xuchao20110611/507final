# Readme for 507 final Project xuchaozj
## api key
OpenWeather Current & Forecast weather data collection API(https://openweathermap.org/api/)

My api code is set in finalsecrets.py and put the file in the .gitignore list, if you want to run the code,
please apply for an api with your edu mail and replace api_key with your own api key.

Or you could run the code by commenting out the follow code in 507final.py:
```

WeatherTree=makeWeatherDict()
json_str1 = json.dumps(WeatherTree, indent=4, cls=EventEncoder)
with open('WeatherTree.json', 'w') as json_file:
    json_file.write(json_str1)
json_file.close()
```
In this way you could only get the weather data from the json file.

## Required Environment
Flask           2.0.2

requests        2.26.0

time            1.0.0

Datetime        4.3.0

bs4             0.0.1

matplotlib      3.5.1

numpy           1.21.4

pandas          1.3.5


##How to run the code
I highly recommend you yo run with IDE like Pycharm to avoid the path error.
Open the root direction within Pycharm and run 507final.py

##Data Structure
There are basically two trees which are both implemented as dict.
One for date weather information and the other for events. 

For the weather tree:

Each day will be separated by city, weather type, temperature type.
For example, all clear days in Boston with high temperature( mintemperature
bigger than 77) will be stored at the same leaf in a list.

For the events tree:

Events in each city will be stored in the same leaf as a list.

##Interacting with the APP
There are four functionalities available on my Flask App. They are separately Temperature Forecast, Daytime Forecast, Humidity Forecast, Travel Recommendations for Boston, Los Angeles, Miami, New York, San Fransisco and Washington DC. When the App is launched, access http://127.0.0.1:5000/ and now you are at the home page. 

Temperature Forecast: 
You could see the forecast temperatures for the following 16 days in your assigned city which are displayed as a line chart. Click on the first hyperlink and redirect to the temperature site:
And in the city chosen page for temperature forecast, Click on the city you want to check, and you could see the line chart for 16 days temperature prediction.

Daytime Forecast:
Click on the second hyperlink in the homepage and redirect to the day time site, and then select the city you are interested in, the UI are almost the same as temperature prediction, and you could see the line chart for 16 days day length prediction and sunrise, sunset times.

Humidity Forecast:
Click on the third hyperlink in the homepage and redirect to the humidity site, and then select the city you are interested in, the UI are almost the same as former two sites, and you could see the line chart for 16 days humidity prediction.

Travel Recommendations:
Click on the fourth hyperlink and you will be redirected to the site for travel recommendation, set your preference for your travel plan and then submit. You could decide the target city, preferred weather type and temperature for your travel plan.
Based on your input form, it will be redirected to three websites, one for the case you do not choose all three required options, one for the case there is no day based on your input and one for successful results.