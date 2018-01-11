from datetime import datetime

print('Note: In order for this to work, the readWeatherData.py file must have been running first, since more than 10 seconds before midnight.')

#Will send an email from 'sendFromEmail' to emails in array 'emailsToSendTo' with specified message and subject.
#Subject is excluded if defined as 'None'
def sendEmail(sendFromEmail,password,subject,messageToSend,emailsToSendTo):
    import smtplib
    from email.mime.text import MIMEText

    #content of email
    msg = MIMEText(messageToSend)

    #if subject isn't equal to 'None'
    if subject != "None":
        msg['Subject'] = subject

    #set email to send from
    msg['From'] = sendFromEmail

    #login to email through smtp server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sendFromEmail,password)

    #send email with specified message and subject to each email in array emailsToSendTo
    for i in emailsToSendTo:
        msg['To'] = i
        text = msg.as_string()
        server.sendmail(sendFromEmail,i,text)

    #exit server
    server.quit()

#returns date as a string in the format d-m-y
def getDateStr(day,month,year):
    return str(day)+'-'+str(month)+'-'+str(year)

#I need these variables to be global, so I define them here
fromEmail = ''
fromEmailPswd = ''
subject = ''
toEmails = []

#get information to send daily data updates to
while True:
    #use input function to define the message variables
    fromEmail = str(input("Email to send updates from: "))
    fromEmailPswd = str(input("Password of "+fromEmail+": "))
    subject = str(input("Subject of email: "))

    #add as many emails as you want to toEmails
    while True:
        toEmails.append(str(input("Email to send data to: ")))
        q = str(input("Want to send to an additional email (y/n)? ")).lower()
        if q == "n" or q == 'no':
            break

    #Verify that the collected information is what the user intended
    print('')
    print('Sending email from '+fromEmail)
    print('Password for '+fromEmail+' is '+fromEmailPswd)
    print('Subject for data email is \"'+subject+'\"')
    print('Emails to send data to:')
    for i in toEmails:
        print('  '+i)
        
    q = str(input('Is this correct? (y/n) ')).lower()
    #if it is correct...
    if q == 'y' or q == 'yes':
        break
    #if it isn't correct, reset toEmails. All the other relevant variables don't need resetting
    else:
        toEmails = []

#tell user the script has started checking to see if the date has changed yet
print('')
print('Started wait')
print('')
print('The script ends only when you press ctrl+c')
print('')

#current date and time
t = datetime.now()
#current date, the date the data file was created
data_date = getDateStr(t.day,t.month,t.year)
while True:
    #update current date and time
    t = datetime.now()
    #update current time, get in a string
    date = getDateStr(t.day,t.month,t.year)

    #if date data was created isn't the same as the current date,
    if data_date != date:
        #open data file and get its contents
        rawData = open('Data/'+data_date+'.txt').readlines()
        data = ''

        #for each line in the data file
        for i in rawData:
            #add the line to 'data' with a linebreak at the end
            data += str(i)+'\n'

        #send the email from the specified email with the specified subject, to the specified emails, with the data from the data file
        sendEmail(fromEmail,fromEmailPswd,subject,data,toEmails)

        #notify user that the email was sent
        print('')
        print('Email sent with weather data for '+data_date)

        #update date for data file
        data_date = getDateStr(t.day,t.month,t.year)
        
        
