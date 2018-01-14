<<<<<<< HEAD
#!/usr/bin/python
import sys
import json
import time
from datetime import datetime
import os

#original source: http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi_3.html

#returns date as a string in the format d-m-y
def getDateStr(day,month,year):
    return str(day)+'-'+str(month)+'-'+str(year)

#server - 'smtp.gmail.com'
#files - [filepath,filepath]
def sendEmail(server,sendFromEmail,password,subject,messageToSend,files,emailToSendTo):
    #import a bunch of stuff
    import smtplib
    import os
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    from email import encoders

    #set up email content
    msg = MIMEMultipart()
    msg['From'] = sendFromEmail
    sg['To'] = COMMASPACE.join(emailToSendTo)
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject

    msg.attach(MIMEText(Text))

    #attach attachments
    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="{0}"'.format(os.path.basename(f)))

    #send email
    send = smtplib.SMTP(server, port)
    if isTLS: send.starttls()
    send.login(sendFromEmail,password)
    send.sendmail(sendFromEmail,emailToSendTo,msg.as_String())

#current date and time
t = datetime.now()
#current date, the date the data file was created
data_date = getDateStr(t.day,t.month,t.year)
buff = ''
while True:    
    try:
        #update current date and time
        t = datetime.now()
        #update current time, get in a string
        date = getDateStr(t.day,t.month,t.year)
        #set filepath name
        filepath = '/home/pi/Desktop/AcuRite-Connection-Stuff/Data/'+data_date+'.txt'

        #if date data was created isn't the same as the current date,
        if data_date != date:
            #get data for email
            emailData = open('emailData.txt').readlines()

            #send the email from the specified email with the specified subject, to the specified emails, with the data from the data file
            sendEmail(emailData[0],emailData[1],emailData[2],emailData[3],emailData[4],[filepath],emailData[3])

            #update date for data file
            data_date = getDateStr(t.day,t.month,t.year)
        
        buff += sys.stdin.read(1)
        if buff.endswith('\n'):
            #get the new data
            data = json.loads(buff[:-1])

            #open file for the day
            if os.path.exists(filepath):
                f = open(filepath, 'a')
            else:
                f = open(filepath, 'w')
                f.close()
                f = open(filepath, 'a')
                os.chown(filepath, 1000, -1)

            #append data at the end
            f.write('date:'+date+' '+str(t.hour)+':'+str(t.minute)+':'+str(t.second)+',wind speed:'+str(data['windSpeed']['WS'])+',wind direction'+str(data['windDirection']['WD'])+',temperature:'+str(data['temperature']['T'])+',humidity:'+str(data['humidity']['H'])+',rain counter:'+str(data['rainCounter']['RC']))
            #close the file
            f.close()

            #shut it down
            sys.stdout.flush()
            buff = ''
    except KeyboardInterrupt:
        #shut it down
        sys.stdout.flush()
        sys.exit()
=======
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
>>>>>>> 0fba3a867b74424d28353e048180ea977802c102
