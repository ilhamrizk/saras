from django.shortcuts import render
import cleartmsi
import os

def output(cleartmsi):
   os.system("mkdir /home/action/david")
   return render(cleartmsi,'subscribers.html')
