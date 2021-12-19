
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

with open("WeatherTree.json",'r') as load_f:
    WeatherTree = json.load(load_f)

load_f.close()
for city in WeatherTree:
    print(city)
    for weather in WeatherTree[city]:
        print('\t',weather)
        for temp in WeatherTree[city][weather]:
            print('\t\t',temp)
            print('\t\t\t',WeatherTree[city][weather][temp])


with open("EventsTree.json",'r') as load_f:
    EventsTree = json.load(load_f)

load_f.close()

for city in EventsTree:
    print(city)
    print('\t',EventsTree[city])