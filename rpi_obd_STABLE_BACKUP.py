from tkinter.constants import ALL, NONE
from tkinter.font import BOLD
import obd
import time
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int
import tkinter as tk 
from tkinter import Label, filedialog, Text 
import tkinter.ttk
import os 
import sys
from bluetooth import * 

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


loop = False
gauge_sweep_bool = False
max_boost = 10.0
min_boost = -10
min_gauge = 220
max_gauge = -40
grey_zone = 0
red_zone = 5
gauge_color = "grey15"
grey_zone_color = "grey30"
nominal_color = "DarkOrange1"
red_zone_color = "red"
gauge_sweep_1 = 220
gauge_sweep_2 = -40
intake = 0
barometric = 0
secondary = 0
grey_zone_arc = (grey_zone - min_boost)/(max_boost - min_boost)
red_zone_arc = (red_zone - min_boost)/(max_boost - min_boost)
arc_length_1 = (grey_zone_arc*(max_gauge - min_gauge))+ min_gauge
arc_length_1 = round(arc_length_1, 2)
arc_length_2 = ((red_zone_arc*(max_gauge - min_gauge))+ min_gauge) 
arc_length_2 = round(arc_length_2, 2)

connection = obd.Async(portstr="/dev/rfcomm0", baudrate=None, protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False)
#connection = obd.Async(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 

def intake_pressure_tracker(a):
    global intake
    if not a.is_null():
        intake = int(a.value.magnitude)
        #print(intake)

def barometric_pressure_tracker(b):
    global barometric
    if not b.is_null():
        barometric = int(b.value.magnitude)
        #print(barometric)

def secondary_tracker(c):
    global secondary
    if not c.is_null():
        secondary = int(c.value.magnitude)
        #print(secondary)


connection.watch(obd.commands.INTAKE_PRESSURE, force=True, callback=intake_pressure_tracker)
connection.watch(obd.commands.BAROMETRIC_PRESSURE, force=True, callback=barometric_pressure_tracker)
connection.watch(obd.commands.COOLANT_TEMP, force=True, callback=secondary_tracker)

root = tk.Tk()
root.attributes('-fullscreen', True)
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


canvas.pack()

JEM = tk.PhotoImage(file="JEM logo.gif")

def close(event):
    root.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing


  

while loop == False:
    if gauge_sweep_bool == False:
        canvas.create_image(240, 240, image = JEM )
        canvas.update()
        canvas.update_idletasks()
        time.sleep(2)
        canvas.delete(ALL)
        gauge_sweep_bool = True
    elif gauge_sweep_1 > -40:
        gauge_sweep_1 = (gauge_sweep_1 -2)
        
        if gauge_sweep_1 ==0:
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_1 , end= gauge_sweep_1-1)
        
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        

    elif gauge_sweep_1 <= -40 and gauge_sweep_2 >= -40 and gauge_sweep_2 <=220:
        gauge_sweep_2 = (gauge_sweep_2 + 2)
      
        if gauge_sweep_2 ==0:
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_2 , end= gauge_sweep_2-1)
       
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        
        
    elif gauge_sweep_1 <= -40 and gauge_sweep_2 >= 220:
       
        canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        canvas.update()
        canvas.update_idletasks()
        loop = True
        connection.start()
      
   

while loop ==True:
    root.bind('<Escape>', close)
    connection.query(obd.commands.INTAKE_PRESSURE, force=True) 
    connection.query(obd.commands.BAROMETRIC_PRESSURE, force=True)
    connection.query(obd.commands.RPM, force=True)
    boost = ((intake - barometric)*0.145038)   #units of kilopascals to psi
    boost = round(boost, 2) # float is truncated to 2 decimals with round()
    temp = (boost - min_boost)/(max_boost - min_boost)

    arc_length_3 = ((temp*(max_gauge - min_gauge))+ min_gauge)
    arc_length_3 = round(arc_length_3, 2)
    
    
    canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
    canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
    canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
    canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
    canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
    canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
    canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
    boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
    boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
    boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
    
    
    if boost <= min_boost:
        
        lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=min_gauge -1, end=min_gauge) #leading arc for aesthetics
        
    elif boost < grey_zone:
        boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_3)
        lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics
       
    elif boost > grey_zone and boost < red_zone:
        boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start= arc_length_1 , end= arc_length_3)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end= arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start= arc_length_3 , end= arc_length_3-1) #leading arc for aesthetics
        
    elif boost > red_zone and boost < max_boost:
        boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= red_zone_color, width=50, start=arc_length_2 , end=arc_length_3)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start=arc_length_1 , end=arc_length_2)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics
       
    elif boost >= max_boost:
        boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= red_zone_color, width=50, start=arc_length_2, end=max_gauge)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start=arc_length_1, end=arc_length_2)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=max_gauge , end=max_gauge-1) #leading arc for aesthetics
        
    
    boost_text = canvas.create_text(240, 240, text=boost, fill="white", font=("Helvetica", 80, 'bold'))
    other_text = canvas.create_text(240, 400, text=secondary, fill="white", font=("Helvetica", 60, 'bold'))
    boost_label = canvas.create_text(240, 300, text="Boost Pressure (PSI)", fill="white", font=("Helvetica", 10, 'bold'))
    other_label = canvas.create_text(240, 440, text="Coolant Temp (C)", fill="white", font=("Helvetica", 10, 'bold'))
    canvas.update()
    canvas.update_idletasks()

    #print(boost) 
    #print(arc_length_1)
    #print(arc_length_2)
    #print(arc_length_3)
    #print(oil_temp)
    #canvas.delete(boost_arc_1)
    #canvas.delete(boost_arc_2)
    #canvas.delete(boost_arc_3)
    #canvas.delete(boost_text)
    canvas.delete(ALL)
    time.sleep(0.033)


