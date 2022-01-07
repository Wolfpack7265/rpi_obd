import obd
import time
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int
loop = True
connection = obd.OBD(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 
intake = obd.commands.INTAKE_PRESSURE
barometric = obd.commands.BAROMETRIC_PRESSURE

while True:
   
    intake_response = connection.query(intake)
    barometric_response = connection.query(barometric)
    boost = (intake_response.value.magnitude - barometric_response.value.magnitude)*0.145038 #units of kilopascals tp psi
    print(round(boost, 2)) # float is truncated to 2 decimals with round()
    time.sleep(1)
