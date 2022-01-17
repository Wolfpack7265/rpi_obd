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

loop = False
gauge_sweep_bool = False
connection = obd.OBD(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 
#connection = obd.OBD()
intake = obd.commands.INTAKE_PRESSURE
barometric = obd.commands.BAROMETRIC_PRESSURE
oil_temp = obd.commands.OIL_TEMP
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

grey_zone_arc = (grey_zone - min_boost)/(max_boost - min_boost)
red_zone_arc = (red_zone - min_boost)/(max_boost - min_boost)
arc_length_1 = (grey_zone_arc*(max_gauge - min_gauge))+ min_gauge
arc_length_1 = round(arc_length_1, 2)
arc_length_2 = ((red_zone_arc*(max_gauge - min_gauge))+ min_gauge) 
arc_length_2 = round(arc_length_2, 2)

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


canvas.pack()

JEM = tk.PhotoImage(file="JEM logo.gif")
  

while loop == False:
    if gauge_sweep_bool == False:
        canvas.create_image(240, 240, image = JEM )   
        canvas.update()
        canvas.update_idletasks()
        time.sleep(2)
        canvas.delete(ALL)
        gauge_sweep_bool = True
    elif gauge_sweep_1 > -40:
        gauge_sweep_1 = (gauge_sweep_1 -10)
        canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
        #canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
        if gauge_sweep_1 ==0:
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_1 , end= gauge_sweep_1-1)
        
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(lead_arc)
        

    elif gauge_sweep_1 == -40 and gauge_sweep_2 >= -40 and gauge_sweep_2 <=215:
        gauge_sweep_2 = (gauge_sweep_2 + 20)
        canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
        if gauge_sweep_2 ==0:
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_2 , end= gauge_sweep_2-1)
       
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(lead_arc)
        
        
    elif gauge_sweep_1 == -40 and gauge_sweep_2 == 220:
       
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
   

while loop ==True:
    
    intake_response = connection.query(intake)
    barometric_response = connection.query(barometric)
    boost = ((intake_response.value.magnitude - barometric_response.value.magnitude)*0.145038) + 10   #units of kilopascals to psi
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
        
    
    boost_text = canvas.create_text(240, 240, text=boost, fill="white", font=("ds-digital", 100, 'bold'))
   # other_text = canvas.create_text(240, 400, text=oil_temp, fill="white", font=("ds-digital", 40, 'bold'))
    canvas.update()
    canvas.update_idletasks()

   # print(boost) 
    #print(arc_length_1)
    #print(arc_length_2)
    #print(arc_length_3)
   # print(oil_temp)
    canvas.delete(boost_arc_1)
    canvas.delete(boost_arc_2)
    canvas.delete(boost_arc_3)
    canvas.delete(boost_text)
    canvas.delete(lead_arc)
    time.sleep(0.10)


