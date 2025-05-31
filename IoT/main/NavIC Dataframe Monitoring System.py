from tkinter import*
import tkinter as tk
import random
import time

root = tk.Tk()
root.geometry("1600x800+0+0")
root.title("NavIC Monitor App _Abhinaba   Version:1.0/2019   PYTHON@ MAC iOS/LINUX/UBUNTU/WINDOWS")




lblInfo=Label(root,font=('arial' , 40 , 'bold'),text="NavIC NMEA_Frame Monitoring Interface",fg="Steel Blue",bd=10, anchor='w',)
lblInfo.grid(row=0,column=0)

#-----------------------LOCAL TIME------------------#
localtime=time.asctime(time.localtime(time.time()))

lblInfo=Label(root,font=('arial' , 20 , 'bold'),text=localtime ,fg="Steel Blue",bd=10, anchor='w')
lblInfo.grid(row=0,column=1)

#-----------------------LOCAL TIME------------------#


def qExit():
    root.destroy()

def Reset():
    lat.set(" ")
    long.set(" ")
    utc.set(" ")
    altitude.set(" ")
    satellites.set(" ")
    fix.set(" ")
    dilution.set(" ")
    geoid.set(" ")
    dgps.set(" ")
    status.set(" ")
    mode.set(" ")
    track.set(" ")
    speed.set(" ")
    variation.set(" ")
    alert.set(" ")
#-----------------------DATA DISPLAYS--------------#

lat = StringVar()
long = StringVar()
utc = StringVar()
altitude = StringVar()
satellites = StringVar()
fix = StringVar()
dilution = StringVar()
geoid = StringVar()
dgps = StringVar()
status = StringVar()
mode = StringVar()
track = StringVar()
speed = StringVar()
variation = StringVar()
alert = StringVar()

lblReference = Label(font=('arial' , 16 , 'bold') , text="Latitude" , bd=10 , anchor='w')
lblReference.grid(row=3,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= lat, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=3,column=1)

lblReference = Label(font=('arial' , 16 , 'bold') , text="Longitude" , bd=10 , anchor='w')
lblReference.grid(row=5,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= long, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=5,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="UTC" , bd=10 , anchor='w')
lblReference.grid(row=7,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= utc, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=7,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="Altitude" , bd=10 , anchor='w')
lblReference.grid(row=9,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= altitude, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=9,column=1)

lblReference = Label(font=('arial' , 16 , 'bold') , text="Satellites" , bd=10 , anchor='w')
lblReference.grid(row=11,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= satellites, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=11,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="Fix Quality" , bd=10 , anchor='w')
lblReference.grid(row=13,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= fix, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=13,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="Horizontal Dilution" , bd=10 , anchor='w')
lblReference.grid(row=15,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= dilution, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=15,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="Height of geoid" , bd=10 , anchor='w')
lblReference.grid(row=17,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= geoid, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=17,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="DGPS Update" , bd=10 , anchor='w')
lblReference.grid(row=19,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= dgps, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=19,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="Status" , bd=10 , anchor='w')
lblReference.grid(row=21,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= status, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=21,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="Mode" , bd=10 , anchor='w')
lblReference.grid(row=23,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= mode, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=23,column=1)


lblReference = Label(font=('arial' , 16 , 'bold') , text="Good Track" , bd=10 , anchor='w')
lblReference.grid(row=25,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= track, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=25,column=1)

lblReference = Label(font=('arial' , 16 , 'bold') , text="Ground Speed (in Knots)" , bd=10 , anchor='w')
lblReference.grid(row=27,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= speed, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=27,column=1)

lblReference = Label(font=('arial' , 16 , 'bold') , text="Magnetic Variation" , bd=10 , anchor='w')
lblReference.grid(row=29,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= variation, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=29,column=1)

lblReference = Label(font=('arial' , 16 , 'bold') , text="Alert & Message" , bd=10 , anchor='w')
lblReference.grid(row=31,column=0)
txtReference=Entry(font=('arial' , 16 ,'bold') , textvariable= alert, bd=10 , insertwidth=4,
                   bg="powder blue" , justify = 'right' , state=DISABLED)
txtReference.grid(row=31,column=1)

#-----------------------DATA DISPLAYS--------------#

#-----------------------NMEA DATA Logging---------------#


#-----------------------NMEA DATA Logging---------------#


#------------------Buttons-----------------------#

btnReset=Button(padx=16,pady=8, bd=16 ,fg="black", font=('arial' , 16 , 'bold'), width=10,
                text="RESET", bg="powder blue" , relief=RIDGE , command = Reset).grid(row=0,column=20)


btnExit=Button(padx=16,pady=8, bd=16 ,fg="black", font=('arial' , 16 , 'bold'), width=10,
                text="QUIT", bg="powder blue" , relief=RIDGE , command = qExit).grid(row=0,column=25)

#------------------Buttons-----------------------#
root.mainloop()
