import influxdb
import os
import string 
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from time import sleep
from datetime import datetime

def datagpsrespack(respackno):
    HOST = 'localhost'
    PORT = '8086'
    USER = 'action'
    PASSWORD = 'action'
    if (respackno==1): #Untuk RESPACK 1
        DBNAME = 'RESPACK1'
    elif(respackno==2): #Untuk RESPACK 2
        DBNAME = 'RESPACK2'
    elif(respackno==3): #UNTUK RESPACK 3
        DBNAME = 'RESPACK3'
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

# def datagpsrespack2():
#     HOST = 'localhost'
#     PORT = '8086'
#     USER = 'action'
#     PASSWORD = 'action'
#     DBNAME = 'RESPACK2'
#         # get last coordinate from database
        
#     queryString = "select * from coordinate group by * order by asc "
#     try:
#         client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
#     except:
#         print("membuat client tidak terberhasilkan")

#     result = client.query(queryString)
#         #print(result)
#     points = result.get_points(tags={'hostname': 'action'})
#     location=[]
#     for coordinate in points:
#         #print(coordinate) 
#         location.append( { "lat" : coordinate['latitude'],
#                 "lng" : coordinate['longitude']})
#     #print(location)
#     return location
    
# def datagpsrespack3():
#     HOST = 'localhost'
#     PORT = '8086'
#     USER = 'action'
#     PASSWORD = 'action'
#     DBNAME = 'RESPACK3'
#         # get last coordinate from database
        
#     queryString = "select * from coordinate group by * order by asc "
#     try:
#         client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
#     except:
#         print("membuat client tidak terberhasilkan")

#     result = client.query(queryString)
#         #print(result)
#     points = result.get_points(tags={'hostname': 'action'})
#     location=[]
#     for coordinate in points:
#         #print(coordinate) 
#         location.append( { "lat" : coordinate['latitude'],
#                 "lng" : coordinate['longitude']})
#     #print(location)
#     return location
# #print (datagpspets())
