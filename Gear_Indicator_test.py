import math 
import time 
import random
vehicle = 1
gears = 0
mk7_golf_automatic = [0.63246, 4.46, 2.51, 1.56, 1.14, 0.85, 0.67]
jk_jeep_wrangler_manual = [1, 4.46, 2.61, 1.72, 1.25, 1, 0.767]
test_car = [1, 1, 2, 3, 4, 5, 6, 7, 8]
calculated_gear_ratio = 0
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
engine_rpm = 0
speed_kmh = 0
tolerance = 0.02
loop = False

def calculate():
    if calculated_gear_ratio > (first_gear - tolerance) and calculated_gear_ratio < (first_gear + tolerance):
        print("1")
    elif calculated_gear_ratio > (second_gear - tolerance) and calculated_gear_ratio < (second_gear + tolerance):
        print("2")
    elif calculated_gear_ratio > (third_gear - tolerance) and calculated_gear_ratio < (third_gear + tolerance):
        print("3")
    elif calculated_gear_ratio > (fourth_gear - tolerance) and calculated_gear_ratio < (fourth_gear + tolerance):
        print("4")
    elif calculated_gear_ratio > (fifth_gear - tolerance) and calculated_gear_ratio < (fifth_gear + tolerance):
        print("5")
    elif calculated_gear_ratio > (sixth_gear - tolerance) and calculated_gear_ratio < (sixth_gear + tolerance):
        print("6")
    elif calculated_gear_ratio > (seventh_gear - tolerance) and calculated_gear_ratio < (seventh_gear + tolerance):
        print("7")
    elif calculated_gear_ratio > (eigth_gear - tolerance) and calculated_gear_ratio < (eigth_gear + tolerance):
        print("8")
    elif calculated_gear_ratio > (ninth_gear - tolerance) and calculated_gear_ratio < (ninth_gear + tolerance):
        print("9")
    elif calculated_gear_ratio > (tenth_gear - tolerance) and calculated_gear_ratio < (tenth_gear + tolerance):
        print("10")
    
    else:
        print("N")



while loop == False:
    if vehicle == 1:
        vehicle = mk7_golf_automatic
    elif vehicle == 2:
        vehicle = jk_jeep_wrangler_manual
    elif vehicle == 3:
        vehicle = test_car
    gears = len(vehicle) - 1
    print(gears)
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
    
    print(tire_size)
    print(first_gear)
    print(second_gear)
    print(third_gear)
    print(fourth_gear)
    print(fifth_gear)
    print(sixth_gear)
    print(seventh_gear)
    print(eigth_gear)
    print(ninth_gear)
    print(tenth_gear)
    loop = True

while loop == True:
    #engine_rpm = random.randint(800, 7000)
    #speed_kmh = random.randint(1, 150)
    calculated_gear_ratio = ((engine_rpm)*(tire_size)*0.06)/(speed_kmh)
    time.sleep(1)
    #calculate()
    print(calculated_gear_ratio)

