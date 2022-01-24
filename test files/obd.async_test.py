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

def new_rpm(r):
    print (r.value)

connection.watch(obd.commands.RPM, callback=new_rpm)
connection.start()

# the callback will now be fired upon receipt of new values

time.sleep(60)
connection.stop()