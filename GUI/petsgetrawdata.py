import influxdb
import os
import string 
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from time import sleep
from datetime import datetime



def read_coordinaterawdata():
    try:
        HOST = '172.27.0.4'
        PORT = '8086'
        USER = 'action'
        PASSWORD = 'action'
        DBNAME = 'PETS'
        # get last coordinate from database
        
        queryString = "select * from coordinate group by * order by asc "
        try:
            client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
        except:
            print("membuat client tidak terberhasilkan")

        result = client.query(queryString)
        #print(result)
        points = result.get_points(tags={'hostname': 'action'})
        lokasiraw=[]
        for coordinate in points:
            #print(coordinate) 
            lokasiraw.append({"lat": coordinate['latitude'],
                    "lng": coordinate['longitude']})
        return lokasiraw
    except:
        return [{"lat": 0.0,
                    "lng": 0.0}]

    
