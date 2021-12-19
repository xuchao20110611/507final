from flask import Flask,render_template,request
import requests


from time import strftime
from time import gmtime
from datetime import datetime

from bs4 import BeautifulSoup
from finalsecrets import api_key

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import json
from json import JSONEncoder




class Day():

    def __init__(self,day,city,mintemperature,maxtemperature,humidity,weather,weatherdetail,sunrise,sunset,daytime):
        self.Day=day
        self.City=city
        self.minTemperature=mintemperature
        self.maxTemperature=maxtemperature
        self.Humidity=humidity
        self.Weather=weather
        self.Sunrise=sunrise
        self.Sunset=sunset
        self.WeatherDetail=weatherdetail
        self.DayTime=daytime

        if maxtemperature<50:
            self.Temp='cold'
        elif mintemperature>77:
            self.Temp='hot'
        else:
            self.Temp='median'

    def __str__(self):
        return str(self.Day)

    def details(self):
        print("For the city " + self.City + " on the day " + self.Day +":\n" \
              + "The minimum temperature: " + str(self.minTemperature) + " The maximum temperature: "+str(self.maxTemperature) +":\n" \
              + "The humidity is " + str(self.Humidity) + " And the weather condition is " + str(self.Weather) +":\n" \
              + "The sun rise at " +str(self.Sunrise) + " and goes down at: " + str(self.Sunset) +":\n" \
              + "The whole day lasts " + str(self.DayTime) + " hours. \n" \
              + "After all, it is a " + self.Temp +" day.")


class Event():
    def __init__(self,title,city,price,description,rating,supplier,src,duration,activitytype):
        self.Title=title
        self.City=city
        self.Price=price
        self.Description=description
        self.Rating=rating
        self.Supplier=supplier
        self.Src=src
        self.Duration=duration
        self.ActivityType=activitytype

        if 'walking' in self.ActivityType:
            self.isRain=False
        else:
            self.isRain=True

        if 'hour' in self.ActivityType or 'min' in self.ActivityType:
            self.ActivityType=None

    def details(self):
        print("The activity "+self.Title + " in " + self.City +" costs " + self.Price )



class EventEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


CityList={'Los Angeles':"https://www.tripadvisor.com/Attraction_Products-g32655-zfg42-Los_Angeles_California.html", \
          'New York':"https://www.tripadvisor.com/Attraction_Products-g60763-zfg42-New_York_City_New_York.html",  \
          'Boston':"https://www.tripadvisor.com/Attraction_Products-g60745-zfg42-Boston_Massachusetts.html", \
          'San Fransisco':"https://www.tripadvisor.com/Attraction_Products-g60713-zfg42-San_Francisco_California.html", \
          'Washington DC':"https://www.tripadvisor.com/Attraction_Products-g28970-zfg42-Washington_DC_District_of_Columbia.html", \
          'Miami':"https://www.tripadvisor.com/Attraction_Products-g34438-zfg42-Miami_Florida.html"}


def makeWeatherDict():
    WeatherTree=dict()
    for city in CityList:
        requestWeather(city=city,WeatherTree=WeatherTree)
    #print(WeatherTree)
    return WeatherTree


def requestWeather(city,WeatherTree):
    base_url = 'http://api.openweathermap.org/data/2.5/forecast/daily'
    params = {'appid': api_key,'cnt':16,'q':city,'units':'imperial'}
    results = requests.get(base_url,params=params).json()
    DaysForcast=results['list']


    for DayWeather in DaysForcast:
        day=DayWeather['dt']
        day=strftime("%d/%m/%y", gmtime(day))
        sunrise = strftime("%H:%M:%S", gmtime(DayWeather['sunrise']))
        sunset = strftime("%H:%M:%S", gmtime(DayWeather['sunset']))

        newday=Day(day=day,city=city,mintemperature=DayWeather['temp']['min'],maxtemperature=DayWeather['temp']['max'],humidity=DayWeather['humidity'],weather=DayWeather['weather'][0]['main'],weatherdetail=DayWeather['weather'][0]['description'],sunrise=sunrise,sunset=sunset,daytime=(DayWeather['sunset']-DayWeather['sunrise'])/3600)
        #newday.details()
        if city not in WeatherTree:
            WeatherTree[city]=dict()
        if newday.Weather not in WeatherTree[city]:
            WeatherTree[city][newday.Weather]=dict()
        if newday.Temp not in WeatherTree[city][newday.Weather]:
            WeatherTree[city][newday.Weather][newday.Temp]=list()
        WeatherTree[city][newday.Weather][newday.Temp].append(newday)
    #print(len(DaysForcast))



headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Course-Info': 'https://www.si.umich.edu/programs/courses/507'}


EventsTree=dict()
def makeEventsTree(city):
    baseURL=CityList[city]
    print("start",city)


    response = requests.get(baseURL,headers=headers)
    print(response.status_code)


    soup = BeautifulSoup(response.text, 'html.parser')
    eventsParent=soup.find('div',attrs={"data-part": "ListSections"})
    event_listing_divs = eventsParent.find_all('section',attrs={"data-automation": "WebPresentation_SingleFlexCardSection"}, recursive=False)


    #testsrc=event_listing_divs[0].find('div',class_='fVbwn cdAAV cagLQ eZTON dofsx').find_all('a',recursive=False)
    for event in event_listing_divs:

        src="https://www.tripadvisor.com"+event.find('a',attrs={"target":"_blank"})['href']
        price=event.find(attrs={"data-automation": "cardPrice"}).contents[0]
        supplier = event.find('header').find_all('a',attrs={"target":"_blank"})[-1].contents[0][3:]



        newpage=requests.get(src,headers=headers)
        newsoup = BeautifulSoup(newpage.text, 'html.parser')
        #print(newsoup.find('h1',attrs={"data-automation": "mainH1"}))
        title = newsoup.find('h1',attrs={"data-automation": "mainH1"}).contents[0]
        description = newsoup.find('div',attrs={"data-automation": "WebPresentation_PoiAboutWeb"}).find('span').find('span').contents[0]
        duration= newsoup.find('div',attrs={"data-automation": "WebPresentation_PoiAboutWeb"}).find('li').contents[0].contents[0]
        duration=duration[10:]
        #supplier = newsoup.find(attrs={"data-automation":"WebPresentation_PoiOverviewWeb"}).find('span').find_all('span')[2].contents[0].contents[0][3:]
        #print(supplier)
        rating = event.find('article').contents[1].find('svg')

        if rating is not None:
            rating = float(rating['aria-label'].split()[0])

        activitytype = event.find('article').contents[1].contents[1].find('div', class_='WlYyy diXIH fPixj').contents[0]



        newEvent=Event(title=title,city=city,price=price,description=description,rating=rating,supplier=supplier,src=src,duration=duration,activitytype=activitytype)

        if city not in EventsTree:
            EventsTree[city] = list()
        EventsTree[city].append(newEvent)
        #print(json.dumps(newEvent,indent=4, cls=EventEncoder))


        #newEvent.details()

        #print(activitytype)
    return EventsTree





WeatherTree=makeWeatherDict()
json_str1 = json.dumps(WeatherTree, indent=4, cls=EventEncoder)
with open('WeatherTree.json', 'w') as json_file:
    json_file.write(json_str1)
json_file.close()
for city in CityList:
    makeEventsTree(city)


json_str = json.dumps(EventsTree, indent=4, cls=EventEncoder)
with open('EventsTree.json', 'w') as json_file:
    json_file.write(json_str)
json_file.close()