import influxdb
import os
import string 
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from time import sleep
from datetime import datetime

def datagpspets():
    HOST = 'localhost'
    PORT = '8086'
    USER = 'action'
    PASSWORD = 'action'
    DBNAME = 'PETS1'
        # get last coordinate from database
        
    queryString = "select * from coordinate group by * order by asc "
    try:
        client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
    except:
        print("membuat client tidak terberhasilkan")

    
    result = client.query(queryString)
        #print(result)
    points = result.get_points(tags={'hostname': 'action'})
    location=[]
    for coordinate in points:
        #print(coordinate) 
        location.append( { "lat" : coordinate['latitude'],
                "lng" : coordinate['longitude']})
    #print(location)
    
    return location

#print (datagpspets())

def datagpspetswarning():
    HOST = 'localhost'
    PORT = '8086'
    USER = 'action'
    PASSWORD = 'action'
    DBNAME = 'PETS1'
        # get last coordinate from database
        
    queryString = "select * from coordinate group by * order by asc "
    try:
        client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
    except:
        print("membuat client tidak terberhasilkan")

    
    result = client.query(queryString)
        #print(result)
    points = result.get_points(tags={'hostname': 'action'})
    warning=[]
    aman=[]
    for coordinate in points:
        if(coordinate['korban']=='warning'):
            warning.append( { "lat" : coordinate['latitude'],
                "lng" : coordinate['longitude']})
    #print(location)
    
    return warning

#print (datagpspets())