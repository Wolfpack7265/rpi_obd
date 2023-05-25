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
import random
from bluetooth import * 

#python3 -m elm -s car

if os.environ.get('DISPLAY','') == '': # sets display
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


loop = False
gauge_sweep_1_bool = False
max_boost = 12
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
nominal_zone = 8
red_zone = 10
gauge_area = (max_gauge - min_gauge)
gauge_increment = gauge_area / max_boost
gauge_increment_values = range(max_boost+1)
gauge_color = "grey15" #"grey15"
needle_color = "red3"
negative_zone_color = "black"
grey_zone_color = "white" #"grey30"
nominal_zone_color = "DarkOrange1"
red_zone_color = "red"
increment_color = "white"
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
nominal_zone_arc = (nominal_zone - min_boost)/(max_boost - min_boost)
red_zone_arc = (red_zone - min_boost)/(max_boost - min_boost)
arc_length_1 = (grey_zone_arc*(max_gauge_negative - min_gauge_negative))+ min_gauge_negative
arc_length_1 = round(arc_length_1, 2)
arc_length_2 = ((nominal_zone_arc*(max_gauge - min_gauge))+ min_gauge) 
arc_length_2 = round(arc_length_2, 2)
arc_length_3 = ((red_zone_arc*(max_gauge - min_gauge))+ min_gauge) 
arc_length_3 = round(arc_length_3, 2)
old_value = min_boost_negative
new_value = min_boost_negative
increment_value = 0
current_value = 0
i=0
increments = 65
launch = False
start_timer_bool = True
start_time = 0
end_time = 0
liters_remaining = 0
vehicle = 1
gears = 0
current_gear = 0
mk7_golf_automatic = [0.63246, 4.46, 2.51, 1.56, 1.14, 0.85, 0.67]
jk_jeep_wrangler = [1, 4.46, 2.61, 1.72, 1.25, 1, 0.767]
test_car = [1, 1, 2, 3, 4, 5, 6, 7, 8]
calculated_gear_ratio = 0
previous_gear = 0
display_gear = False
delete_gear = False
first_gear = None
second_gear = None
third_gear = None
fourth_gear = None
fifth_gear = None
sixth_gear = None
seventh_gear = None
eigth_gear = None
ninth_gear = None
tenth_gear = None
tolerance = 0.05

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
    x = math.cos(math.radians(angle)) * 165 + 240
    y = math.sin(math.radians(angle)) * 165 + 240
    obj = canvas.create_text(240, 240, text=text, fill= increment_color, font=("Helvetica", 20, 'bold'))
    canvas.coords(obj, x, y)
    return obj
def draw_rotated_text(angle, radius, text, size):
    x = math.cos(math.radians(angle)) * radius + 240
    y = math.sin(math.radians(angle)) * radius + 240
    obj = canvas.create_text(240, 240, text=text, fill="white", font=("Helvetica", size, 'bold'))
    canvas.itemconfig(obj, angle=-angle+90)
    canvas.coords(obj, x, y)
    return obj

def draw_passive_elements():
    canvas.create_circle_arc(240, 240, 238, style="arc", outline= "white", width=4, start=220, end= 180 ) #-40 # outer ring
    for j in gauge_increment_values:
        if j == 0:
            increment_color = "white"
            gauge_increments_black = canvas.create_circle_arc(240, 240, 211, style="arc", outline= "black", width=56, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_top = canvas.create_circle_arc(240, 240, 236, style="arc", outline= increment_color, width=10, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_bottom = canvas.create_circle_arc(240, 240, 190, style="arc", outline= increment_color, width=6, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
        elif j >= 0 and j <= nominal_zone:
            increment_color = "white"
            gauge_increments_black = canvas.create_circle_arc(240, 240, 211, style="arc", outline= "black", width=56, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_top = canvas.create_circle_arc(240, 240, 236, style="arc", outline= increment_color, width=10, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_bottom = canvas.create_circle_arc(240, 240, 190, style="arc", outline= increment_color, width=6, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
        elif j > nominal_zone and j<= red_zone:
            increment_color = nominal_zone_color
            gauge_increments_black = canvas.create_circle_arc(240, 240, 211, style="arc", outline= "black", width=56, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_top = canvas.create_circle_arc(240, 240, 236, style="arc", outline= increment_color, width=10, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_bottom = canvas.create_circle_arc(240, 240, 190, style="arc", outline= increment_color, width=6, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
        elif j > red_zone:
            increment_color = red_zone_color
            gauge_increments_black = canvas.create_circle_arc(240, 240, 211, style="arc", outline= "black", width=56, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_top = canvas.create_circle_arc(240, 240, 236, style="arc", outline= increment_color, width=10, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
            gauge_increments_bottom = canvas.create_circle_arc(240, 240, 190, style="arc", outline= increment_color, width=6, start=180 + (gauge_increment*j), end=180 + (gauge_increment*j)-1)
        outer_ring=canvas.create_circle_arc(240, 240, 238, style="arc", outline= increment_color, width=4, start=180 + (gauge_increment*(j-1)), end=180 + (gauge_increment*j ))
        inner_ring=canvas.create_circle_arc(240, 240, 186, style="arc", outline= increment_color, width=2, start=180 + (gauge_increment*(j-1)), end=180 + (gauge_increment*(j) ))
        negative_cover = canvas.create_circle_arc(240, 240, 186, style="arc", outline= "black", width=4, start=220, end= 180 ) # inner ring negative cover 
        #canvas.tag_raise(gauge_increments)
        draw_increments(180 - (gauge_increment*j),j)
    min_boost = canvas.create_text(110, 340, text="-10", fill= "white", font=("Helvetica", 20, 'bold')) # min boost 
    left_endstop = canvas.create_circle_arc(240, 240, 215, style="arc", outline= "white", width=60, start=220, end=222) # left endstop
    right_endstop = canvas.create_circle_arc(240, 240, 215, style="arc", outline= red_zone_color, width=60, start=320, end=318) # right endstop
    fuel_endstop = canvas.create_circle_arc(240, 240, 225, style="arc", outline= "white", width=25, start=max_gauge_fuel, end=max_gauge_fuel -1) # fuel endstop
    boost_text = canvas.create_text(240, 130, text="Boost Pressure (PSI)", fill= "white", font=("Helvetica", 10, 'bold')) # boost text
    fuel_percent = draw_rotated_text(408, 225, '%', 20) # percent of fuel level 
    global gear_text
    gear_text = canvas.create_text(240, 240, text=current_gear, fill= "black", font=("Helvetica", 1, 'bold'))
    #intake_text = draw_rotated_text(127, 195, 'Intake:', 15) # "intake" text
    #intake_degrees = draw_rotated_text(102, 195, "°C", 15) # "°C" text
    #coolant_text = draw_rotated_text(75, 195, 'Coolant:', 15) # "coolant" text
    #coolant_degrees = draw_rotated_text(47, 195, "°C", 15) # "°C" text

def fuel_gauge(fuel):
    global fuel_bar, fuel_bar_arc
    temp_fuel = fuel_level/100
    arc_length_fuel = ((temp_fuel*(max_gauge_fuel - min_gauge_fuel))+ min_gauge_fuel)
    arc_length_fuel = round(arc_length_fuel, 2)
    if fuel >= 100:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= "forestgreen", width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)
    elif fuel < 100 and fuel > 25:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= "grey30", width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)
    elif fuel <= 25 and fuel >10:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= nominal_zone_color, width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)
    elif fuel <= 10:
        fuel_bar = canvas.create_circle_arc(240, 240, 225, style="arc", outline= red_zone_color, width=25, start=222, end=arc_length_fuel)
        fuel_bar_arc = canvas.create_circle_arc(240, 240, 225, style="arc", outline="white", width=25, start=arc_length_fuel , end=arc_length_fuel-1)

def compute_gear_ratio(calculated_gear_ratio):
    global current_gear
    
    if first_gear != None and calculated_gear_ratio > (first_gear - tolerance) and calculated_gear_ratio < (first_gear + tolerance):
        current_gear = 1  
    elif second_gear != None and calculated_gear_ratio > (second_gear - tolerance) and calculated_gear_ratio < (second_gear + tolerance):
        current_gear = 2  
    elif third_gear != None and calculated_gear_ratio > (third_gear - tolerance) and calculated_gear_ratio < (third_gear + tolerance):
        current_gear = 3  
    elif fourth_gear != None and calculated_gear_ratio > (fourth_gear - tolerance) and calculated_gear_ratio < (fourth_gear + tolerance):
        current_gear = 4  
    elif fifth_gear != None and calculated_gear_ratio > (fifth_gear - tolerance) and calculated_gear_ratio < (fifth_gear + tolerance):
        current_gear = 5  
    elif sixth_gear != None and calculated_gear_ratio > (sixth_gear - tolerance) and calculated_gear_ratio < (sixth_gear + tolerance):
        current_gear = 6  
    elif seventh_gear != None and calculated_gear_ratio > (seventh_gear - tolerance) and calculated_gear_ratio < (seventh_gear + tolerance):
        current_gear = 7   
    elif eigth_gear != None and calculated_gear_ratio > (eigth_gear - tolerance) and calculated_gear_ratio < (eigth_gear + tolerance):
        current_gear = 8   
    elif ninth_gear != None and calculated_gear_ratio > (ninth_gear - tolerance) and calculated_gear_ratio < (ninth_gear + tolerance):
        current_gear = 9  
    elif tenth_gear != None and calculated_gear_ratio > (tenth_gear - tolerance) and calculated_gear_ratio < (tenth_gear + tolerance):
        current_gear = 10   
    else:
        current_gear = 0
        


root = tk.Tk()
root.attributes('-fullscreen', True)
canvas = tk.Canvas(root, width=480, height=480, borderwidth=0, highlightthickness=0,
bg="black")



canvas.grid()

root.title("rpi_obd")

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



def gauge_sweep():
    global gauge_sweep_1_bool, gauge_sweep_1_start_point, gauge_sweep_1_end_point, loop, lead_arc
    if gauge_sweep_1_bool == False:
        canvas.create_image(240, 240, image = JEM )
        canvas.update()
        canvas.update_idletasks()
        time.sleep(2)
        canvas.delete(ALL)
        draw_passive_elements()
        gauge_sweep_1_bool = True
    elif gauge_sweep_1_start_point > max_gauge:
        gauge_sweep_1_start_point = (gauge_sweep_1_start_point -1)
        time.sleep(0.004)
        if gauge_sweep_1_start_point ==0:
            lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=50, start=2 , end= 2 -2)
        else:
            lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=50, start=gauge_sweep_1_start_point , end= gauge_sweep_1_start_point-2)
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(lead_arc)

    elif gauge_sweep_1_start_point <= max_gauge and gauge_sweep_1_end_point >= max_gauge and gauge_sweep_1_end_point <= min_gauge_negative:
        gauge_sweep_1_end_point = (gauge_sweep_1_end_point + 1)
        time.sleep(0.004)
        if gauge_sweep_1_end_point ==0:
            lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=50, start=2 , end= 2 -2)
        else:
            lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=50, start=gauge_sweep_1_end_point , end= gauge_sweep_1_end_point-2)
        canvas.update()
        canvas.update_idletasks()
        canvas.delete(lead_arc)
        
    elif gauge_sweep_1_start_point <= max_gauge and gauge_sweep_1_end_point >= min_gauge_negative:
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
        connection.watch(obd.commands.COOLANT_TEMP, callback=coolant_temp_tracker)
        connection.watch(obd.commands.FUEL_LEVEL, callback=fuel_level_tracker)
        connection.watch(obd.commands.SPEED, callback=speed_tracker)
        connection.watch(obd.commands.RPM, callback=rpm_tracker)
        connection.start()
        draw_passive_elements()
        
connection.query(obd.commands.INTAKE_PRESSURE, force=True) 
connection.query(obd.commands.BAROMETRIC_PRESSURE, force=True)

while loop == False:
    if vehicle == 1:
        vehicle = mk7_golf_automatic
    elif vehicle == 2:
        vehicle = jk_jeep_wrangler
    elif vehicle == 3:
        vehicle = test_car
    gears = len(vehicle) - 1
    if gears == 5:
        tire_size = vehicle[0]
        first_gear = vehicle[1]
        second_gear = vehicle[2]
        third_gear = vehicle[3]
        fourth_gear = vehicle[4]
        fifth_gear = vehicle[5]
    elif gears == 6:
        tire_size = vehicle[0]
        first_gear = vehicle[1]
        second_gear = vehicle[2]
        third_gear = vehicle[3]
        fourth_gear = vehicle[4]
        fifth_gear = vehicle[5]
        sixth_gear = vehicle[6]
    elif gears == 7:
        tire_size = vehicle[0]
        first_gear = vehicle[1]
        second_gear = vehicle[2]
        third_gear = vehicle[3]
        fourth_gear = vehicle[4]
        fifth_gear = vehicle[5]
        sixth_gear = vehicle[6]
        seventh_gear = vehicle[7]
    elif gears == 8:
        tire_size = vehicle[0]
        first_gear = vehicle[1]
        second_gear = vehicle[2]
        third_gear = vehicle[3]
        fourth_gear = vehicle[4]
        fifth_gear = vehicle[5]
        sixth_gear = vehicle[6]
        seventh_gear = vehicle[7]
        eigth_gear = vehicle[8]
    elif gears == 9:
        tire_size = vehicle[0]
        first_gear = vehicle[1]
        second_gear = vehicle[2]
        third_gear = vehicle[3]
        fourth_gear = vehicle[4]
        fifth_gear = vehicle[5]
        sixth_gear = vehicle[6]
        seventh_gear = vehicle[7]
        eigth_gear = vehicle[8]
        ninth_gear = vehicle[9]
    elif gears == 10:
        tire_size = vehicle[0]
        first_gear = vehicle[1]
        second_gear = vehicle[2]
        third_gear = vehicle[3]
        fourth_gear = vehicle[4]
        fifth_gear = vehicle[5]
        sixth_gear = vehicle[6]
        seventh_gear = vehicle[7]
        eigth_gear = vehicle[8]
        ninth_gear = vehicle[9]
        tenth_gear = vehicle[10]
    gauge_sweep()
   
while loop ==True:   
    root.bind('<Escape>', close)
    boost = ((intake - barometric)*0.145038)#units of kilopascals to psi
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
        arc_length_4 = ((temp*(max_gauge_negative - min_gauge_negative))+ min_gauge_negative)
        arc_length_4 = round(arc_length_4, 2)

    elif (current_value > 0):
        temp = (current_value - min_boost)/(max_boost - min_boost)
        arc_length_4 = ((temp*(max_gauge - min_gauge))+ min_gauge)
        arc_length_4 = round(arc_length_4, 2)

    fuel_gauge(fuel_level)
    fuel_text = draw_rotated_text(417, 225, fuel_level, 20) # text for fuel level
    #intake_value = draw_rotated_text(109, 195, intake_temp, 15) # text for intake
    #coolant_value = draw_rotated_text(54, 195, coolant_temp, 15) # text for coolant

    if current_value <= min_boost_negative:
        boost_arc_4 = boost_arc_3 = boost_arc_2 = boost_arc_1 = lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width= 58, start=min_gauge_negative -2, end=min_gauge_negative)
        canvas.tag_lower(lead_arc)
    elif current_value < grey_zone:
        boost_arc_4 =boost_arc_3 = boost_arc_2 = boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end=arc_length_4)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        #lead_arc = canvas.create_circle_arc(240, 240, 128, style="arc", outline=needle_color, width=216, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        #boost_arc_3 = boost_arc_2 = boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=220, end=arc_length_4)
        canvas.tag_lower(boost_arc_1)
    elif current_value == 0:
        boost_arc_4 = boost_arc_3 = boost_arc_2 = boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end=arc_length_4)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        canvas.tag_lower(boost_arc_1)
    
    elif current_value > grey_zone and current_value < nominal_zone:
        boost_arc_4 =boost_arc_3 = boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start= arc_length_1 , end= arc_length_4)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end= arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        #boost_arc_3 = boost_arc_2 = canvas.create_circle_arc(240, 240, 213, style="arc", outline= nominal_color, width=54, start= arc_length_2 , end= arc_length_4)
        canvas.tag_lower(boost_arc_1)
        canvas.tag_lower(boost_arc_2)

    elif current_value == nominal_zone:
        boost_arc_4 = boost_arc_3 = boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start= arc_length_1 , end= arc_length_2)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end=arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        canvas.tag_lower(boost_arc_1)
        canvas.tag_lower(boost_arc_2)
    
    elif current_value > nominal_zone and current_value < red_zone:
        boost_arc_4 = boost_arc_3 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_zone_color, width=50, start=arc_length_2 , end=arc_length_4)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=arc_length_1 , end=arc_length_2)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end=arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        canvas.tag_lower(boost_arc_1)
        canvas.tag_lower(boost_arc_2)
        canvas.tag_lower(boost_arc_3)
    
    elif current_value == red_zone :
        boost_arc_4 = boost_arc_3 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_zone_color, width=50, start=arc_length_2 , end=arc_length_4)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=arc_length_1 , end=arc_length_2)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end=arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        canvas.tag_lower(boost_arc_1)
        canvas.tag_lower(boost_arc_2)
        canvas.tag_lower(boost_arc_3)
    
    elif current_value > red_zone and current_value < max_boost:
        boost_arc_4 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= red_zone_color, width=50, start=arc_length_3 , end=arc_length_4)
        boost_arc_3 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_zone_color, width=50, start=arc_length_2 , end=arc_length_3)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=arc_length_1 , end=arc_length_2)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end=arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        canvas.tag_lower(boost_arc_1)
        canvas.tag_lower(boost_arc_2)
        canvas.tag_lower(boost_arc_3)
        canvas.tag_lower(boost_arc_4)
        
    
    elif current_value >= max_boost:
        boost_arc_4 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= red_zone_color, width=50, start=arc_length_3 , end=max_gauge)
        boost_arc_3 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= nominal_zone_color, width=50, start=arc_length_2, end=arc_length_3)
        boost_arc_2 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= grey_zone_color, width=50, start=arc_length_1, end=arc_length_2)
        boost_arc_1 = canvas.create_circle_arc(240, 240, 211, style="arc", outline= negative_zone_color, width=50, start=220, end=arc_length_1)
        lead_arc = canvas.create_circle_arc(240, 240, 211, style="arc", outline=needle_color, width=58, start=arc_length_4 , end=arc_length_4-2) #leading arc for aesthetics
        canvas.tag_lower(boost_arc_1)
        canvas.tag_lower(boost_arc_2)
        canvas.tag_lower(boost_arc_3)
        canvas.tag_lower(boost_arc_4)
    
    if rpm > 2100 and speed != 0:
        #calculated_gear_ratio = vehicle[random.randint(1, 6)]
        calculated_gear_ratio = ((rpm)*(tire_size)*0.06)/(speed)
        compute_gear_ratio(calculated_gear_ratio)
        #print(current_gear, previous_gear)
        if current_gear > 0 and previous_gear != current_gear:
            previous_gear = current_gear
            display_gear = True
        elif current_gear > 0 and previous_gear == current_gear:
            display_gear = False

        if display_gear == False and delete_gear == False:
            gear_text = canvas.create_text(240, 240, text=current_gear, fill= "white", font=("Helvetica", 110, 'bold')) 
            delete_gear = True

    

    canvas.update()
    canvas.update_idletasks()
    canvas.delete(boost_arc_1)
    canvas.delete(boost_arc_2)
    canvas.delete(boost_arc_3)
    canvas.delete(boost_arc_4)
    canvas.delete(lead_arc)
    canvas.delete(fuel_bar)
    canvas.delete(fuel_bar_arc)
    canvas.delete(fuel_text)
    if display_gear == True:
        canvas.delete(gear_text)
        delete_gear = False
    #canvas.delete(intake_value)
    #canvas.delete(coolant_value)
    #time.sleep(0.005)