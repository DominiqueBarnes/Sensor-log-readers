from tkinter import *
import matplotlib.pyplot as plt
import dropbox
import datetime
from SensorClass import Sensor

gui = Tk()
gui.geometry('400x250')
gui.title('Logs Reader')

reminder = Message(gui,text = 'Remember to update gui.py, line 79 with your access token.',width=400, bg='light blue')
reminder.grid(row=6,columnspan=3, pady=10)

begindatelabel = Label(gui, text='Enter start date (YYYY-MM-DD):')
begindatelabel.grid(column=0, row=1)

enddatelabel = Label(gui, text='Enter end date (YYYY-MM-DD):')
enddatelabel.grid(column=0, row=2)

# Take user-input dates and store them as datetime objects
begindateentry = Entry(gui,width=10)
begindateentry.grid(column=1,row=1)
begindateentry.focus()

enddateentry = Entry(gui,width=10)
enddateentry.grid(column=1,row=2)

listboxlabel = Label(gui, text='Select sensor data to plot:', padx=10)
listboxlabel.grid(column=2,row=0)

listbox = Listbox(gui, selectmode=MULTIPLE, bg='yellow')
listbox.grid(column=2,row=1, padx=10, rowspan=3)

listbox.insert(1,'Conductivity')
listbox.insert(2,'Ammonia')
listbox.insert(3,'Dissolved Oxygen')
listbox.insert(4,'Nitrate')
listbox.insert(5,'pH')
listbox.insert(6,'Turbidity')
listbox.insert(7,'COD')
listbox.insert(8,'Temperature')

def selectall():
    listbox.select_set(0, END)

allbutton = Button(gui, text='Select all', command=selectall)
allbutton.grid(row=4,column=2)

def plot():
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
    access = 'paste access token here'
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

plotbutton = Button(gui, text="Plot", command=plot)
plotbutton.grid(row=3, column=0)

def closegui():
    gui.quit()
    
closebutton = Button(gui, text="Close", command=closegui)
closebutton.grid(row=3,column=1)