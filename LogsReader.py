import matplotlib.pyplot as plt
import dropbox
import datetime
from gui import *
from SensorClass import Sensor

gui.mainloop()

dates = []

begindate = begindateentry.get()
datecounter = datetime.datetime.strptime(begindate, '%Y-%m-%d')

enddate = enddateentry.get()
endcounter = datetime.datetime.strptime(enddate, '%Y-%m-%d')

while datecounter <= endcounter: #Loop until the datecounter exceeds the enddate
    date = datecounter.strftime('%Y-%m-%d') #Make a string of the date in the form YYYY-MM-DD
    dates.insert(0,date) #Add the date to the list, 'dates'
    datecounter += datetime.timedelta(days=1) #Add 1 day to the datecounter

CONDset = [] #Conductivity
AMMset = [] #Ammonia
DOset = [] #Dissolved Oxygen
NITset = [] #Nitrate
pHset = [] #pH
TURBset = [] #Turbidity
CODset = [] #Carbon Oxygen Demand
TEMPset = [] #Temperature
tset = [] #Timestamps

sensorset = [CONDset, AMMset,DOset,NITset,pHset,TURBset,CODset,TEMPset]
nameset = ['Conductivity','Ammonia','DO','Nitrate','pH','Turbidity','COD','Temperature']
colorset = ['cyan','gold','blue','limegreen','darkviolet','sienna','red','gray']
ylabelset = ['mS/cm','mg/L','mg/L','mg/L','pH','mg/L','mg/L','$^\circ$ C']

#Import and read .csv file from Dropbox
access = 'n4YZi1o2-rAAAAAAAAAAF7TD9ZMa3uCHek2JNPhWeegaV3RsOipC0TAIMXZ4mge4'
dbx = dropbox.Dropbox(access)

for date in dates:
    md, res = dbx.files_download('/P3/logs/backlog/sensor_log_' + date + '.csv')
    data = res.text
    lines = data.split('\n')

    for line in lines:
        s = line.split('\t')
        try:
            y = int(s[0][0:4])
            m = int(s[0][5:7])
            d = int(s[0][8:10])
            hr = int(s[0][11:13])
            mn = int(s[0][14:16])
        except:
            continue
        for sensor in sensorset:
            try:
                point = float(s[sensorset.index(sensor)+1])
            except: point = 0
            sensor.append(point)
        tset.append(datetime.datetime(y,m,d,hr,mn))
        
selected = listbox.curselection()
numselected = len(selected)

sensors = []

for selection in selected:
    sensor = Sensor(sensorset[selection],nameset[selection],colorset[selection],ylabelset[selection])
    sensors.append(sensor)

fig = plt.figure()
plt.suptitle('Sensor hub data '+begindate+' - '+enddate)

if numselected <= 2:
    for sensor in sensors:
        plt.subplot (numselected,1,sensors.index(sensor)+1)
        plt.plot(tset, sensor.sensor, color=sensor.color)
        plt.title(sensor.name, color = sensor.color)
        plt.ylabel(sensor.ylabel, color = sensor.color)
        plt.xlabel('Timestamp')
else:
    for sensor in sensors:
        rows = round(numselected/2)
        plt.subplot (rows,2,sensors.index(sensor)+1)
        plt.plot(tset, sensor.sensor, color=sensor.color)
        plt.title(sensor.name, color = sensor.color)
        plt.ylabel(sensor.ylabel, color = sensor.color)
        plt.xlabel('Timestamp')

fig.autofmt_xdate()
fig.tight_layout(h_pad=0.1,w_pad=0.2)

plt.show()
