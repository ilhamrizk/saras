import influxdb
import string 
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from time import sleep
from datetime import datetime
import os

def read_coordinate(respackno):
    if (respackno==1): #Untuk RESPACK 1
        HOST = '172.27.0.1'
    elif(respackno==2): #Untuk RESPACK 2
        HOST = '172.27.0.2'
    elif(respackno==3): #UNTUK RESPACK 3
        HOST = '172.27.0.3'
    PORT = '8086'
    USER = 'action'
    PASSWORD = 'action'
    DBNAME = 'RESPACK'
    # get last coordinate from database
    
    queryString = "select * from coordinate group by * order by asc "
    try:
        client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
    except:
        print("membuat client tidak terberhasilkan")

    result = client.query(queryString)
    #print(result)
    points = result.get_points(tags={'hostname': 'action'})
    test=[]
    for coordinate in points:
        #print(coordinate) 
        test.append({"latitude": coordinate['latitude'],
                "longitude": coordinate['longitude'],"time": coordinate['time']})
    return test

    
def write_coordinate(gpsData,respackno):
    HOST1 = 'localhost'
    PORT1 = '8086'
    USER1 = 'action'
    PASSWORD1 = 'action'
    if (respackno==1): #Untuk RESPACK 1
        DBNAME1 = 'RESPACK1'
    elif(respackno==2): #Untuk RESPACK 2
        DBNAME1 = 'RESPACK2'
    elif(respackno==3): #UNTUK RESPACK 3
        DBNAME1 = 'RESPACK3'

    for x in gpsData:
        time = x.get('time')
        #print(time)
        #time = now().strftime("%Y-%m-%dT%H:%M:%SZ")
        metric = "coordinate"
        hostname = "action"
        #print(x)
        pointValue = [{
               "time": time,
               "measurement": metric,
               "fields":  {
                   "latitude": x.get('latitude'),
                   "longitude": x.get('longitude')
              },
                'tags': {
                    "hostname": hostname
               }
            }] 
        
        #print(pointValue)
     
        client1 = InfluxDBClient(HOST1, PORT1, USER1, PASSWORD1, DBNAME1)
        
        (client1.write_points(pointValue))
               
os.system("sudo sh /etc/saras/mesh.sh")
gps_data1=read_coordinate(1)
print("berhasil baca koordinat RESPACK 1")
gps_data2=read_coordinate(2)
print("berhasil baca koordinat RESPACK 2")
gps_data3=read_coordinate(3)
print("berhasil baca koordinat RESPACK 3")
write_coordinate(gps_data1,1)
print("berhasil write coor 1")
write_coordinate(gps_data2,2)
print("berhasil write coor 2")
write_coordinate(gps_data3,3)
print("berhasil write coor 3")