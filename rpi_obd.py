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
import math
#from bluetooth import * 

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


loop = False
gauge_sweep_1_bool = False
gauge_sweep_2_bool = False
max_boost = 10.0
min_boost = -10
min_gauge = 220
max_gauge = -40
min_gauge_2 = 175
max_gauge_2 = 5
grey_zone = 0
red_zone = 5
gauge_color = "grey15"
grey_zone_color = "grey30"
nominal_color = "DarkOrange1"
red_zone_color = "red"
gauge_sweep_1_start_point = 220
gauge_sweep_1_end_point = -40
gauge_sweep_2_start_point = 175
gauge_sweep_2_end_point = 5
intake = 0
intake_temp = 0
barometric = 0
coolant_temp = 0
speed = 0
fuel_level = 0
rpm = 0
grey_zone_arc = (grey_zone - min_boost)/(max_boost - min_boost)
red_zone_arc = (red_zone - min_boost)/(max_boost - min_boost)
arc_length_1 = (grey_zone_arc*(max_gauge - min_gauge))+ min_gauge
arc_length_1 = round(arc_length_1, 2)
arc_length_2 = ((red_zone_arc*(max_gauge - min_gauge))+ min_gauge) 
arc_length_2 = round(arc_length_2, 2)
old_value = min_boost
new_value = 0
increment_value = 0
current_value = 0
i=0
increments = 10
mode = 0
launch = False
start_timer_bool = True
start_time = 0
end_time = 0

#connection = obd.Async(portstr="/dev/rfcomm0", baudrate=None, protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False)
connection = obd.Async(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 

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

def coolant_temp_tracker(c):
    global coolant_temp
    if not c.is_null():
        coolant_temp = int(c.value.magnitude)
        #print(coolant_temp)

def speed_tracker(d):
    global speed
    if not d.is_null():
        speed = int(d.value.magnitude)
        #print(speed)

def intake_temp_tracker(e):
    global intake_temp
    if not e.is_null():
        intake_temp = int(e.value.magnitude)
        #print(intake_temp)

def fuel_level_tracker(f):
    global fuel_level
    if not f.is_null():
        fuel_level= int(f.value.magnitude)
        #print(fuel_level)

def rpm_tracker(g): 
    global rpm 
    if not g.is_null():
        rpm = int(g.value.magnitude)
        #print(rpm )



#connection.watch(obd.commands.INTAKE_PRESSURE, force=True, callback=intake_pressure_tracker)
#connection.watch(obd.commands.BAROMETRIC_PRESSURE, force=True, callback=barometric_pressure_tracker)
#connection.watch(obd.commands.COOLANT_TEMP, force=True, callback=coolant_temp_tracker)
#connection.watch(obd.commands.SPEED, force=True, callback=speed_tracker)
#connection.watch(obd.commands.INTAKE_TEMP, force=True, callback=intake_temp_tracker)
#connection.watch(obd.commands.FUEL_LEVEL, force=True, callback=fuel_level_tracker)

root = tk.Tk()
#root.attributes('-fullscreen', True)
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

def mode_switch(event):
    global mode
    if mode == 0:
        mode +=1
        connection.stop()
        connection.watch(obd.commands.INTAKE_PRESSURE, force=True, callback=intake_pressure_tracker)
        connection.watch(obd.commands.BAROMETRIC_PRESSURE, force=True, callback=barometric_pressure_tracker)
        connection.watch(obd.commands.INTAKE_TEMP, force=True, callback=intake_temp_tracker)
        connection.unwatch(obd.commands.SPEED, callback=speed_tracker)
        connection.unwatch(obd.commands.COOLANT_TEMP, callback=coolant_temp_tracker)
        connection.unwatch(obd.commands.FUEL_LEVEL, callback=fuel_level_tracker)
        connection.unwatch(obd.commands.RPM, callback=rpm_tracker)
        connection.start()
        
    elif mode == 1:
        mode +=1

    elif mode == 2:
        mode = 0
        connection.stop()
        connection.watch(obd.commands.SPEED, force=True, callback=speed_tracker)
        connection.watch(obd.commands.COOLANT_TEMP, force=True, callback=coolant_temp_tracker)
        connection.watch(obd.commands.FUEL_LEVEL, force=True, callback=fuel_level_tracker)
        connection.watch(obd.commands.RPM, force=True, callback=rpm_tracker)
        connection.unwatch(obd.commands.INTAKE_PRESSURE, callback=intake_pressure_tracker)
        connection.unwatch(obd.commands.BAROMETRIC_PRESSURE, callback=barometric_pressure_tracker)
        connection.unwatch(obd.commands.INTAKE_TEMP, callback=intake_temp_tracker)
        connection.start()

def temp_override_mode_switch():
    global mode
    if mode == 0:
        mode = 3
        connection.stop()
        connection.watch(obd.commands.INTAKE_PRESSURE, force=True, callback=intake_pressure_tracker)
        connection.watch(obd.commands.BAROMETRIC_PRESSURE, force=True, callback=barometric_pressure_tracker)
        connection.watch(obd.commands.INTAKE_TEMP, force=True, callback=intake_temp_tracker)
        connection.unwatch(obd.commands.SPEED, callback=speed_tracker)
        connection.unwatch(obd.commands.COOLANT_TEMP, callback=coolant_temp_tracker)
        connection.unwatch(obd.commands.FUEL_LEVEL, callback=fuel_level_tracker)
        connection.start()
        
    elif mode == 3:
        mode = 0
        connection.stop()
        connection.watch(obd.commands.SPEED, force=True, callback=speed_tracker)
        connection.watch(obd.commands.COOLANT_TEMP, force=True, callback=coolant_temp_tracker)
        connection.watch(obd.commands.FUEL_LEVEL, force=True, callback=fuel_level_tracker)
        connection.watch(obd.commands.RPM, force=True, callback=rpm_tracker)
        connection.unwatch(obd.commands.INTAKE_PRESSURE, callback=intake_pressure_tracker)
        connection.unwatch(obd.commands.BAROMETRIC_PRESSURE, callback=barometric_pressure_tracker)
        connection.unwatch(obd.commands.INTAKE_TEMP, callback=intake_temp_tracker)
        connection.start()
        

def normal_mode_gauge_sweep():
    global gauge_sweep_2_bool, gauge_sweep_2_start_point, gauge_sweep_2_end_point, loop, lead_arc
    if gauge_sweep_2_bool == False:
        canvas.create_image(240, 240, image = JEM )
        canvas.update()
        canvas.update_idletasks()
        time.sleep(2)
        canvas.delete(ALL)
        gauge_sweep_2_bool = True
    elif gauge_sweep_2_start_point > 5:
        gauge_sweep_2_start_point = (gauge_sweep_2_start_point -1)
        
        if gauge_sweep_2_start_point ==0:
            #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start= 5, end= 175)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=-15, end=5)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=175, end=195)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start= 5, end= 175)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=-15, end=5)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=175, end=195)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_2_start_point , end= gauge_sweep_2_start_point-1)
        
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        

    elif gauge_sweep_2_start_point <= 5 and gauge_sweep_2_end_point >= 5 and gauge_sweep_2_end_point <=175:
        gauge_sweep_2_end_point = (gauge_sweep_2_end_point + 1)
      
        if gauge_sweep_2_end_point ==0:
           # canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start= 5, end= 175)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=-15, end=5)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=175, end=195)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start= 5, end= 175)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=-15, end=5)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=175, end=195)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_2_end_point , end= gauge_sweep_2_end_point-1)
       
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        
        
    elif gauge_sweep_2_start_point <= 5 and gauge_sweep_2_end_point >= 175:
       
       # canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start= 5, end= 175)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=-15, end=5)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=175, end=195)
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        canvas.update()
        canvas.update_idletasks()
        loop = True
        connection.stop()
        connection.watch(obd.commands.SPEED, force=True, callback=speed_tracker)
        connection.watch(obd.commands.COOLANT_TEMP, force=True, callback=coolant_temp_tracker)
        connection.watch(obd.commands.FUEL_LEVEL, force=True, callback=fuel_level_tracker)
        connection.watch(obd.commands.RPM, force=True, callback=rpm_tracker)
        connection.unwatch(obd.commands.INTAKE_PRESSURE, callback=intake_pressure_tracker)
        connection.unwatch(obd.commands.BAROMETRIC_PRESSURE, callback=barometric_pressure_tracker)
        connection.unwatch(obd.commands.INTAKE_TEMP, callback=intake_temp_tracker)
        connection.start()

def sport_mode_gauge_sweep():
    global gauge_sweep_1_bool, gauge_sweep_1_start_point, gauge_sweep_1_end_point, loop, lead_arc
    if gauge_sweep_1_bool == False:
        canvas.create_image(240, 240, image = JEM )
        canvas.update()
        canvas.update_idletasks()
        time.sleep(2)
        canvas.delete(ALL)
        gauge_sweep_1_bool = True
    elif gauge_sweep_1_start_point > -40:
        gauge_sweep_1_start_point = (gauge_sweep_1_start_point -2)
        
        if gauge_sweep_1_start_point ==0:
            #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_1_start_point , end= gauge_sweep_1_start_point-1)
        
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        

    elif gauge_sweep_1_start_point <= -40 and gauge_sweep_1_end_point >= -40 and gauge_sweep_1_end_point <=220:
        gauge_sweep_1_end_point = (gauge_sweep_1_end_point + 2)
      
        if gauge_sweep_1_end_point ==0:
           # canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=2 , end= 2 -1)
        else:
            #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=gauge_sweep_1_end_point , end= gauge_sweep_1_end_point-1)
       
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        
        
    elif gauge_sweep_1_start_point <= -40 and gauge_sweep_1_end_point >= 220:
       
       # canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
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
        connection.stop()
        connection.watch(obd.commands.INTAKE_PRESSURE, force=True, callback=intake_pressure_tracker)
        connection.watch(obd.commands.BAROMETRIC_PRESSURE, force=True, callback=barometric_pressure_tracker)
        connection.watch(obd.commands.INTAKE_TEMP, force=True, callback=intake_temp_tracker)
        connection.unwatch(obd.commands.SPEED, callback=speed_tracker)
        connection.unwatch(obd.commands.COOLANT_TEMP, callback=coolant_temp_tracker)
        connection.unwatch(obd.commands.FUEL_LEVEL, callback=fuel_level_tracker)
        connection.unwatch(obd.commands.RPM, callback=rpm_tracker)
        connection.start()


connection.query(obd.commands.INTAKE_PRESSURE, force=True) 
connection.query(obd.commands.BAROMETRIC_PRESSURE, force=True)

while loop == False:
    if mode == 0:
        normal_mode_gauge_sweep()
    elif mode == 1:
        sport_mode_gauge_sweep()
   

while loop ==True:
    if mode == 0:
        root.bind('<Escape>', close)
        root.bind('<Return>', mode_switch)
        
        if rpm > 3000:
            mode = 3
            temp_override_mode_switch()

        temp = fuel_level/100
        arc_length_3 = ((temp*(max_gauge_2 - min_gauge_2))+ min_gauge_2)
        arc_length_3 = round(arc_length_3, 2)

        #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start= 5, end= 175)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=-15, end=5)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=175, end=195)
        canvas.create_text(240, 110, text=fuel_level, fill="white", font=("Helvetica", 40, 'bold'))
        canvas.create_text(240, 150, text="Fuel Level (%)", fill="white", font=("Helvetica", 10, 'bold'))
        canvas.create_text(240, 240, text=speed, fill="white", font=("Helvetica", 80, 'bold'))
        canvas.create_text(240, 300, text="Speed (km/h)", fill="white", font=("Helvetica", 10, 'bold'))
        canvas.create_text(240, 400, text=coolant_temp, fill="white", font=("Helvetica", 40, 'bold'))
        canvas.create_text(240, 440, text="Coolant Temp (C)", fill="white", font=("Helvetica", 10, 'bold'))

        if fuel_level > 25:
         canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=175, end=arc_length_3)
         canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1)
         canvas.create_text(40, 260, text="E", fill="white", font=("Helvetica", 40, 'bold'))
         canvas.create_text(440, 260, text="F", fill="white", font=("Helvetica", 40, 'bold'))
         canvas.update()
         canvas.update_idletasks()
         canvas.delete(ALL)

        elif fuel_level <=25 and fuel_level > 10:
         canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start=175, end=arc_length_3)
         canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1)
         canvas.create_text(40, 260, text="E", fill=nominal_color, font=("Helvetica", 40, 'bold'))
         canvas.create_text(440, 260, text="F", fill="white", font=("Helvetica", 40, 'bold'))
         canvas.update()
         canvas.update_idletasks()
         canvas.delete(ALL)
        
        elif fuel_level <=10: 
         canvas.create_circle_arc(240, 240, 205, style="arc", outline= red_zone_color, width=50, start=175, end=arc_length_3)
         canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1)
         canvas.create_text(40, 260, text="E", fill=red_zone_color, font=("Helvetica", 40, 'bold'))
         canvas.create_text(440, 260, text="F", fill="white", font=("Helvetica", 40, 'bold'))
         canvas.update()
         canvas.update_idletasks()
         canvas.delete(ALL)   
        
    elif mode == 1:
        root.bind('<Escape>', close)
        root.bind('<Return>', mode_switch)
        boost = ((intake - barometric)*0.145038)   #units of kilopascals to psi
        boost = round(boost, 2) # float is truncated to 2 decimals with round()

        increment_value = (new_value - old_value)/increments
        if i <increments:
            current_value = old_value + i*(increment_value)
            current_value = round(current_value, 2)
            i+=1
        elif i>=increments:
             old_value = new_value
             new_value = boost
             i = 0
        temp = (current_value - min_boost)/(max_boost - min_boost)

        arc_length_3 = ((temp*(max_gauge - min_gauge))+ min_gauge)
        arc_length_3 = round(arc_length_3, 2)
    
        #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
        boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
    
    
        if current_value <= min_boost:
        
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=min_gauge -1, end=min_gauge) #leading arc for aesthetics
        
        elif current_value < grey_zone:
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_3)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics

        elif current_value == 0:
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_1-1) #leading arc for aesthetics
       
        elif current_value > grey_zone and current_value < red_zone:
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start= arc_length_1 , end= arc_length_3)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end= arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start= arc_length_3 , end= arc_length_3-1) #leading arc for aesthetics

        elif current_value == red_zone:
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start= arc_length_1 , end= arc_length_3)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics
        
        elif current_value > red_zone and current_value < max_boost:
            boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= red_zone_color, width=50, start=arc_length_2 , end=arc_length_3)
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start=arc_length_1 , end=arc_length_2)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics
       
        elif current_value >= max_boost:
            boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= red_zone_color, width=50, start=arc_length_2, end=max_gauge)
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start=arc_length_1, end=arc_length_2)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=max_gauge , end=max_gauge-1) #leading arc for aesthetics
        
    
        boost_text = canvas.create_text(240, 240, text=math.trunc(current_value), fill="white", font=("Helvetica", 80, 'bold'))
        other_text = canvas.create_text(240, 400, text=intake_temp, fill="white", font=("Helvetica", 60, 'bold'))
        boost_label = canvas.create_text(240, 300, text="Boost Pressure (PSI)", fill="white", font=("Helvetica", 10, 'bold'))
        other_label = canvas.create_text(240, 440, text="Intake Temp (C)", fill="white", font=("Helvetica", 10, 'bold'))
        canvas.update()
        canvas.update_idletasks()

        
        canvas.delete(ALL)
        #time.sleep(0.033)

    elif mode == 2:
        root.bind('<Escape>', close)
        root.bind('<Return>', mode_switch)
        connection.query(obd.commands.SPEED, force=True)
        if speed > 0 and launch == False:
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= 220, end= -40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            canvas.create_text(240, 150, text="0-20", fill="white", font=("Helvetica", 40, 'bold'))
            speed_text = canvas.create_text(240, 240, text=speed, fill="white", font=("Helvetica", 80, 'bold'))
            canvas.update()
            canvas.update_idletasks()
            canvas.delete(ALL)
        elif speed == 0 and launch == False:
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= -40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            canvas.create_text(240, 150, text="0-20", fill="white", font=("Helvetica", 40, 'bold'))
            speed_text = canvas.create_text(240, 240, text=speed, fill="white", font=("Helvetica", 80, 'bold'))
            canvas.update()
            canvas.update_idletasks()
            time.sleep(2)
            launch = True
            canvas.delete(ALL)

        elif speed == 0 and launch==True:
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= "green", width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= "green", width=4, start= 220, end= -40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            canvas.create_text(240, 150, text="0-20", fill="white", font=("Helvetica", 40, 'bold'))
            speed_text = canvas.create_text(240, 240, text=speed, fill="white", font=("Helvetica", 80, 'bold'))
            canvas.update()
            canvas.update_idletasks()
            canvas.delete(ALL)
        elif speed >0 and launch==True:
            start = time.time()
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= -40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            canvas.create_text(240, 150, text="0-20", fill="white", font=("Helvetica", 40, 'bold'))
            canvas.create_text(240, 240, text=speed, fill="white", font=("Helvetica", 80, 'bold'))
            canvas.update()
            canvas.update_idletasks()
            canvas.delete(ALL)
        elif speed >=20 and launch==True:
            end = time.time()
            final_time = end - start
            canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start=220, end=-40)
            canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= 220, end= -40)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
            canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
            canvas.create_text(240, 150, text="0-20", fill="white", font=("Helvetica", 40, 'bold'))
            canvas.create_text(240, 240, text=final_time, fill="white", font=("Helvetica", 80, 'bold'))
            canvas.update()
            canvas.update_idletasks()
            time.sleep(10)
            launch = False
            canvas.delete(ALL)
            
    elif mode == 3:
        if rpm < 2000 and start_timer_bool ==True:
            start_time = time.perf_counter()
            start_timer_bool = False 

        elif rpm < 2000 and start_timer_bool == False:
            end_time = time.perf_counter()

        elif rpm > 2000: 
            start_time_bool = True

        if (end_time - start_time) >= 10:
            mode = 0  
            temp_override_mode_switch()
            
        root.bind('<Escape>', close)

        boost = ((intake - barometric)*0.145038)   #units of kilopascals to psi
        boost = round(boost, 2) # float is truncated to 2 decimals with round()

        increment_value = (new_value - old_value)/increments
        if i <increments:
            current_value = old_value + i*(increment_value)
            current_value = round(current_value, 2)
            i+=1
        elif i>=increments:
             old_value = new_value
             new_value = boost
             i = 0
        temp = (current_value - min_boost)/(max_boost - min_boost)

        arc_length_3 = ((temp*(max_gauge - min_gauge))+ min_gauge)
        arc_length_3 = round(arc_length_3, 2)
    
        #canvas.create_circle(240, 240, 230, fill="black", outline= gauge_color, width=4 )
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= gauge_color, width=4, start=220, end=-40)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= grey_zone_color, width=4, start= 220, end= arc_length_1)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= nominal_color, width=4, start= arc_length_1, end= arc_length_2)
        canvas.create_circle_arc(240, 240, 180, style="arc", outline= red_zone_color, width=4, start= arc_length_2, end=-40)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=220, end=230)
        canvas.create_circle_arc(240, 240, 195, style="arc", outline= gauge_color, width=70, start=310, end=320)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
        boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline="grey", width=50, start=220, end=220)
    
    
        if current_value <= min_boost:
        
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=min_gauge -1, end=min_gauge) #leading arc for aesthetics
        
        elif current_value < grey_zone:
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_3)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics

        elif current_value == 0:
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_1-1) #leading arc for aesthetics
       
        elif current_value > grey_zone and current_value < red_zone:
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start= arc_length_1 , end= arc_length_3)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end= arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start= arc_length_3 , end= arc_length_3-1) #leading arc for aesthetics

        elif current_value == red_zone:
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start= arc_length_1 , end= arc_length_3)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics
        
        elif current_value > red_zone and current_value < max_boost:
            boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= red_zone_color, width=50, start=arc_length_2 , end=arc_length_3)
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start=arc_length_1 , end=arc_length_2)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=arc_length_3 , end=arc_length_3-1) #leading arc for aesthetics
       
        elif current_value >= max_boost:
            boost_arc_3 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= red_zone_color, width=50, start=arc_length_2, end=max_gauge)
            boost_arc_2 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= nominal_color, width=50, start=arc_length_1, end=arc_length_2)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 205, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 205, style="arc", outline="white", width=60, start=max_gauge , end=max_gauge-1) #leading arc for aesthetics
        
    
        boost_text = canvas.create_text(240, 240, text=math.trunc(current_value), fill="white", font=("Helvetica", 80, 'bold'))
        other_text = canvas.create_text(240, 400, text=intake_temp, fill="white", font=("Helvetica", 60, 'bold'))
        boost_label = canvas.create_text(240, 300, text="Boost Pressure (PSI)", fill="white", font=("Helvetica", 10, 'bold'))
        other_label = canvas.create_text(240, 440, text="Intake Temp (C)", fill="white", font=("Helvetica", 10, 'bold'))
        canvas.update()
        canvas.update_idletasks()

        
        canvas.delete(ALL)
        
        
       
        
    
    


