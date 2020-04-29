from tkinter import *

gui = Tk()
gui.geometry('400x250')

begindatelabel = Label(gui, text='Enter start date (YYYY-MM-DD):')
begindatelabel.grid(column=0, row=0)

enddatelabel = Label(gui, text='Enter end date (YYYY-MM-DD):')
enddatelabel.grid(column=0, row=1)

# Take user-input dates and store them as datetime objects
begindateentry = Entry(gui,width=10)
begindateentry.grid(column=1,row=0)
begindateentry.focus()

enddateentry = Entry(gui,width=10)
enddateentry.grid(column=1,row=1)

listboxlabel = Label(gui, text='Select sensor data to plot:', padx=10)
listboxlabel.grid(column=2,row=0)

listbox = Listbox(gui, selectmode=MULTIPLE, bg='yellow')
listbox.grid(column=2,row=1, padx=10, rowspan=2)

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

def closegui():
    gui.quit()
    
plotbutton = Button(gui, text="Plot", command=closegui)
plotbutton.grid(row=4)