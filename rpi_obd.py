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
from bluetooth import * 

#python3 -m elm -s car

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


loop = False
gauge_sweep_1_bool = False
max_boost = 10.0
min_boost = 0
max_boost_negative = 0
min_boost_negative= -10
min_gauge = 180
max_gauge = -40
min_gauge_negative = 220
max_gauge_negative = 180
min_gauge_fuel = 222
max_gauge_fuel = 295
grey_zone = 0
red_zone = 5
gauge_area = (max_gauge - min_gauge)
gauge_increment = gauge_area / max_boost
gauge_increment_values = range(11)
gauge_color = "grey15"
grey_zone_color = "black" #"grey30"
nominal_color = "DarkOrange1"
red_zone_color = "red"
gauge_sweep_1_start_point = 220
gauge_sweep_1_end_point = -40
gauge_sweep_2_start_point = 170
gauge_sweep_2_end_point = 10
intake = 0
intake_temp = 0
barometric = 0
coolant_temp = 0
speed = 0
fuel_level = 0
rpm = 0
grey_zone_arc = (grey_zone - min_boost_negative)/(max_boost_negative - min_boost_negative)
red_zone_arc = (red_zone - min_boost)/(max_boost - min_boost)
arc_length_1 = (grey_zone_arc*(max_gauge_negative - min_gauge_negative))+ min_gauge_negative
arc_length_1 = round(arc_length_1, 2)
arc_length_2 = ((red_zone_arc*(max_gauge - min_gauge))+ min_gauge) 
arc_length_2 = round(arc_length_2, 2)
old_value = min_boost
new_value = 0
increment_value = 0
current_value = 0
i=0
increments = 10
launch = False
start_timer_bool = True
start_time = 0
end_time = 0
liters_remaining = 0

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

def draw_increments(angle, text):
    x = math.cos(math.radians(angle)) * 160 + 240
    y = math.sin(math.radians(angle)) * 160 + 240
    obj = canvas.create_text(240, 240, text=text, fill="white", font=("Helvetica", 30, 'bold'))
    canvas.coords(obj, x, y)
    return obj
def draw_rotated_text(angle, radius, text):
    x = math.cos(math.radians(angle)) * radius + 240
    y = math.sin(math.radians(angle)) * radius + 240
    obj = canvas.create_text(240, 240, text=text, fill="white", font=("Helvetica", 20, 'bold'))
    canvas.itemconfig(obj, angle=-angle+90)
    canvas.coords(obj, x, y)
    return obj


def fuel_gauge(fuel):
    global fuel_bar, fuel_bar_arc
    temp_fuel = fuel_level/100
    arc_length_fuel = ((temp_fuel*(max_gauge_fuel - min_gauge_fuel))+ min_gauge_fuel)
    arc_length_fuel = round(arc_length_fuel, 2)
    if fuel >= 75:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= "forestgreen", width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)
    elif fuel < 75 and fuel > 25:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= "grey30", width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)
    elif fuel <= 25 and fuel >10:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= nominal_color, width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)
    elif fuel <= 10:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= red_zone_color, width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)



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



def boost_mode_gauge_sweep():
    global gauge_sweep_1_bool, gauge_sweep_1_start_point, gauge_sweep_1_end_point, loop, lead_arc
    if gauge_sweep_1_bool == False:
        canvas.create_image(240, 240, image = JEM )
        canvas.update()
        canvas.update_idletasks()
        time.sleep(2)
        canvas.delete(ALL)
        gauge_sweep_1_bool = True
    elif gauge_sweep_1_start_point > max_gauge:
        gauge_sweep_1_start_point = (gauge_sweep_1_start_point -2)
        
        if gauge_sweep_1_start_point ==0:
            canvas.create_circle_arc(240, 240, 238, style="arc", outline= "white", width=4, start=220, end=-40 ) # outer ring
            for j in gauge_increment_values:
                canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1) 
                draw_increments(180 - (gauge_increment*j),j)
            canvas.create_text(120, 340, text="-10", fill="white", font=("Helvetica", 30, 'bold')) # min boost 
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=220, end=222) # left endstop
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=320, end=318) # right endstop
            canvas.create_circle(240, 240, 20, fill=gauge_color, outline= "white", width=4 ) # inner circle
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=2 , end= 2 -1)
        else:
            canvas.create_circle_arc(240, 240, 238, style="arc", outline= "white", width=4, start=220, end=-40 ) # outer ring
            for j in gauge_increment_values:
                canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1) 
                draw_increments(180 - (gauge_increment*j),j)
            canvas.create_text(120, 340, text="-10", fill="white", font=("Helvetica", 30, 'bold')) # min boost 
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=220, end=222) # left endstop
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=320, end=318) # right endstop
            canvas.create_circle(240, 240, 20, fill=gauge_color, outline= "white", width=4 ) # inner circle
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=gauge_sweep_1_start_point , end= gauge_sweep_1_start_point-1)
        
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        

    elif gauge_sweep_1_start_point <= max_gauge and gauge_sweep_1_end_point >= max_gauge and gauge_sweep_1_end_point <= min_gauge_negative:
        gauge_sweep_1_end_point = (gauge_sweep_1_end_point + 2)
      
        if gauge_sweep_1_end_point ==0:
            canvas.create_circle_arc(240, 240, 238, style="arc", outline= "white", width=4, start=220, end=-40 ) # outer ring
            for j in gauge_increment_values:
                canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1) 
                draw_increments(180 - (gauge_increment*j),j)
            canvas.create_text(120, 340, text="-10", fill="white", font=("Helvetica", 30, 'bold')) # min boost 
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=220, end=222) # left endstop
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=320, end=318) # right endstop
            canvas.create_circle(240, 240, 20, fill=gauge_color, outline= "white", width=4 ) # inner circle
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="white", width=216, start=2 , end= 2 -1)
        else:
            canvas.create_circle_arc(240, 240, 238, style="arc", outline= "white", width=4, start=220, end=-40 ) # outer ring
            for j in gauge_increment_values:
                canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1) 
                draw_increments(180 - (gauge_increment*j),j)
            canvas.create_text(120, 340, text="-10", fill="white", font=("Helvetica", 30, 'bold')) # min boost 
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=220, end=222) # left endstop
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=320, end=318) # right endstop
            canvas.create_circle(240, 240, 20, fill=gauge_color, outline= "white", width=4 ) # inner circle
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=gauge_sweep_1_end_point , end= gauge_sweep_1_end_point-1)
       
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(ALL)
        
        
    elif gauge_sweep_1_start_point <= max_gauge and gauge_sweep_1_end_point >= min_gauge_negative:
        canvas.create_circle_arc(240, 240, 238, style="arc", outline= "white", width=4, start=220, end=-40 ) # outer ring
        for j in gauge_increment_values:
            canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1) 
            draw_increments(180 - (gauge_increment*j),j)
        canvas.create_text(120, 340, text="-10", fill="white", font=("Helvetica", 30, 'bold')) # min boost 
        canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=220, end=222) # left endstop
        canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=320, end=318) # right endstop
        canvas.create_circle(240, 240, 20, fill=gauge_color, outline= "white", width=4 ) # inner circle
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
        connection.watch(obd.commands.FUEL_LEVEL, callback=fuel_level_tracker)
        connection.unwatch(obd.commands.SPEED, callback=speed_tracker)
        connection.unwatch(obd.commands.COOLANT_TEMP, callback=coolant_temp_tracker)
        connection.unwatch(obd.commands.RPM, callback=rpm_tracker)
        connection.start()
        canvas.create_circle_arc(240, 240, 238, style="arc", outline= "white", width=4, start=220, end=-40 ) # outer ring
        for j in gauge_increment_values:
                canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1) 
                draw_increments(180 - (gauge_increment*j),j)
        canvas.create_text(120, 340, text="-10", fill="white", font=("Helvetica", 30, 'bold')) # min boost 
        canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=220, end=222) # left endstop
        canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=50, start=320, end=318) # right endstop
        canvas.create_circle(240, 240, 20, fill=gauge_color, outline= "white", width=4 ) # inner circle



connection.query(obd.commands.INTAKE_PRESSURE, force=True) 
connection.query(obd.commands.BAROMETRIC_PRESSURE, force=True)

while loop == False:
    boost_mode_gauge_sweep()
   

while loop ==True:   
        root.bind('<Escape>', close)
        boost = ((intake - barometric)*0.145038) #units of kilopascals to psi
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

        if (current_value <=0):
            temp = (current_value - min_boost_negative)/(max_boost_negative - min_boost_negative)
            arc_length_3 = ((temp*(max_gauge_negative - min_gauge_negative))+ min_gauge_negative)
            arc_length_3 = round(arc_length_3, 2)

        elif (current_value > 0):
            temp = (current_value - min_boost)/(max_boost - min_boost)
            arc_length_3 = ((temp*(max_gauge - min_gauge))+ min_gauge)
            arc_length_3 = round(arc_length_3, 2)
    
        boost_label = canvas.create_text(240, 175, text="Boost Pressure (PSI)", fill="white", font=("Helvetica", 10, 'bold'))
        fuel_label = draw_rotated_text(417, 225, fuel_level)
        fuel_percent = draw_rotated_text(408, 225, '%')
        fuel_gauge(fuel_level)
    
        if current_value <= min_boost_negative:
           boost_arc_3 = boost_arc_2 = boost_arc_1 = lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width= 216, start=min_gauge_negative -2, end=min_gauge_negative)
        
        elif current_value < grey_zone:
            boost_arc_3 = boost_arc_2 = boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_3)
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=arc_length_3 , end=arc_length_3-2) #leading arc for aesthetics

        elif current_value == 0:
            boost_arc_3 = boost_arc_2 = boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=arc_length_3 , end=arc_length_1-2) #leading arc for aesthetics
       
        elif current_value > grey_zone and current_value < red_zone:
            boost_arc_3 = boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_color, width=50, start= arc_length_1 , end= arc_length_3)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=220, end= arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start= arc_length_3 , end= arc_length_3-2) #leading arc for aesthetics

        elif current_value == red_zone:
            boost_arc_3 = boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_color, width=50, start= arc_length_1 , end= arc_length_3)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 215, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=arc_length_3 , end=arc_length_3-2) #leading arc for aesthetics
        
        elif current_value > red_zone and current_value < max_boost:
            boost_arc_3 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= red_zone_color, width=50, start=arc_length_2 , end=arc_length_3)
            boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_color, width=50, start=arc_length_1 , end=arc_length_2)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=arc_length_3 , end=arc_length_3-2) #leading arc for aesthetics
       
        elif current_value >= max_boost:
            boost_arc_3 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= red_zone_color, width=50, start=arc_length_2, end=max_gauge)
            boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_color, width=50, start=arc_length_1, end=arc_length_2)
            boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_1)
            lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline="red", width=216, start=max_gauge , end=max_gauge-2) #leading arc for aesthetics
        
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(boost_arc_1)
        canvas.delete(boost_arc_2)
        canvas.delete(boost_arc_3)
        canvas.delete(lead_arc)
        canvas.delete(boost_label)
        canvas.delete(fuel_label)
        canvas.delete(fuel_percent)
        canvas.delete(fuel_bar)
        canvas.delete(fuel_bar_arc)

        #time.sleep(0.033)

   
