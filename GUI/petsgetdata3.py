import influxdb
import os
import string 
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from time import sleep
from datetime import datetime



def read_coordinate():
    HOST = '172.27.0.6'
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
    points = result.get_points(tags={'hostname': 'Tim TA'})
    test=[]
    for coordinate in points:
        #print(coordinate) 
        test.append({"latitude": coordinate['latitude'],
                "longitude": coordinate['longitude'],"time": coordinate['time'],"korban":coordinate['korban'],"metric":coordinate['metric']})
    return test

    
def write_coordinate(gpsData):
    HOST1 = 'localhost'
    PORT1 = '8086'
    USER1 = 'action'
    PASSWORD1 = 'action'
    DBNAME1 = 'PETS1'

    for x in gpsData:
        time = x.get('time')
        #print(time)
        #time = now().strftime("%Y-%m-%dT%H:%M:%SZ")
        metric = "coordinate"
        hostname = "Tim TA"
        #print(x)
        pointValue = [{
               "time": time,
               "measurement": metric,
               "fields":  {
                   "latitude": x.get('latitude'),
                   "longitude": x.get('longitude'),
                   "metric":x.get('metric'),
                   "korban":x.get('korban')
              },
                'tags': {
                    "hostname": hostname
               }
            }] 
        
        #print(pointValue)
     
        client1 = InfluxDBClient(HOST1, PORT1, USER1, PASSWORD1, DBNAME1)
        
        (client1.write_points(pointValue))

#os.system("sudo sh mesh.sh")
gps_data = read_coordinate()
write_coordinate(gps_data)
print("berhasil")
