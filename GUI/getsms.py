import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import glob
import os

def getsms():
    try:
        list_of_files=glob.glob("/run/user/1000/gvfs/mtp:host=%5Busb%3A002%2C016%5D/Phone/SMSToExcel/*.xls")
        latest_file = max(list_of_files, key=os.path.getctime)
        os.system("sudo cp latest_file /home/david/GUI/remote/sms/")
        os.chdir("/home/david/GUI/remote/sms")
        df = pd.read_excel(latest_file, sheet_name='Sheet1')
    except:
        list_of_files=glob.glob("/home/david/GUI/remote/sms/*.xls")
        latest_file = max(list_of_files, key=os.path.getctime)
        os.chdir("/home/david/GUI/remote/sms")
        df = pd.read_excel(latest_file, sheet_name='Sheet1')

    Addresses = df['Address']
    Name = df['Name']
    Date = df['Date']
    Type = df['Type']
    Body = df['Body']
    pesans = []
    for i in df.index:
        pesans.append(
            {
                'ADDRESS' : (Addresses[i]),
                'NAME' : str(Name[i]),
                'DATE' : Date[i],
                'TYPE' : Type[i],
                'BODY' : Body[i]
            }
        )
    return pesans