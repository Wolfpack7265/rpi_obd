import obd
import time
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int
import tkinter as tk 
from tkinter import Label, filedialog, Text 
import os 
loop = True
connection = obd.OBD(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 
intake = obd.commands.INTAKE_PRESSURE
barometric = obd.commands.BAROMETRIC_PRESSURE
max_boost = 10.0
min_boost = -15.0
min_gauge = 220
max_gauge = -40

root = tk.Tk()
canvas = tk.Canvas(root, width=480, height=480, borderwidth=0, highlightthickness=0,
bg="black")



canvas.grid()

root.title("rpi_boost_gauge")

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc

canvas.create_circle(240, 240, 230, fill="black", outline="grey", width=4)

canvas.create_circle_arc(240, 240, 210, style="arc", outline="white", width=40,
                         start=270-50, end=270+50)
#Start of gauge = 270-50, end is 270+50

boost_text = Label(root, text = "boooooost")
boost_text.config(font =("Courier", 30))
canvas.pack()
boost_text.pack()



while True:
    
    intake_response = connection.query(intake)
    barometric_response = connection.query(barometric)
    boost = (intake_response.value.magnitude - barometric_response.value.magnitude)*0.145038 #units of kilopascals tp psi
    boost = round(boost, 2) # float is truncated to 2 decimals with round()
    temp = (boost - min_boost)/(max_boost - min_boost)
    arc_length = (temp*(max_gauge - min_gauge))+ min_gauge
    
    canvas.create_circle_arc(240, 240, 210, style="arc", outline="red", width=40, start=220, end=arc_length)
    canvas.update()
    canvas.update_idletasks()

    print(boost) 
    print(arc_length)
    
    time.sleep(0.5)


