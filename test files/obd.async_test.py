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
#from bluetooth import * 
loop = False

connection = obd.Async(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=5, check_voltage=True, start_low_power=False) 
rpm = 0
def rpmTracker(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.magnitude)
        print(rpm)


connection.watch(obd.commands.RPM, callback=rpmTracker)
connection.start()

while loop == False:
    print(rpm)
    
    time.sleep(0.03)


