#!/usr/bin/python
import sys
import json
import time
from datetime import datetime

#source: http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi_3.html

#notify user that the script has at least started
print("called")

#returns date as a string in the format d-m-y
def getDateStr(day,month,year):
    return str(day)+'-'+str(month)+'-'+str(year)

buff = ''
while True:
    try:
        buff += sys.stdin.read(1)
        if buff.endswith('\n'):
            #store current date and time
            t = datetime.now()
            #get current date as a string
            date = getDateStr(t.day,t.month,t.year)

            #get the new data
            data = json.loads(buff[:-1])

            #open file for the day
            f = open('Data/'+str(t.day)+'-'+str(t.month)+'-'+str(t.year)+'.txt', 'a')
            #append data at the end
            f.write('date:'+str(t.day)+'-'+str(t.month)+'-'+str(t.year)+' '+str(t.hour)+':'+str(t.minute)+':'+str(t.second)+',wind speed:'+str(data['windSpeed']['WS'])+',wind direction'+str(data['windDirection']['WD'])+',temperature:'+str(data['temperature']['T'])+',humidity:'+str(data['humidity']['H'])+',rain counter:'+str(data['rainCounter']['RC']))
            #close the file
            f.close()

            #Notify user that the data file has been updated
            print('Data file last updated on '+date+' at '+str(t.hour)+':'+str(t.minute)+':'+str(t.second))
            
            sys.stdout.flush()
            buff = ''
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys.exit()
