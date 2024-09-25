import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from opensky_api import OpenSkyApi

source="C:\\Users\\todds\\Desktop\\SolarCar\\opensky-api-master\\opensky-api-master\\python\\airports.csv"

from classspec import airport_activity


username=input("username")
password=input("password")

api = OpenSkyApi(username,password)

#airport=input("Airport")

CYYZ=airport_activity("CYYZ",api)


airportname=input()

airport=pd.read_csv(source)
airport = airport.filter(items=['ident', 'latitude_deg', 'longitude_deg'])

minlat,maxlat,minlon,maxlon=CYYZ.find_coordinate(airport)
logbook=[]
while True:
    
    states=CYYZ.get_current_state(minlat,maxlat,minlon,maxlon)
    #print(states)
    df=CYYZ.make_list(states)
    CYYZ.update_list(df)
    time.sleep(300) 
    #in test airport (CYYZ) it is not likely an aircraft spend less than 5 minutes after
    #switching on its transbonder to leave the detection zone given, or to park and switch
    #off its transbonder within 5 minutes entering the detection zone.
    #print(airport_activity.log)
    #airport_activity.log.to_csv('output.csv', index=False)
