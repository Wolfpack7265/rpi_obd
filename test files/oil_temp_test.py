import obd
import time
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int
loop = True
connection = obd.OBD(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 

def oil_temp(messages):
    """decoder for boost messages"""
    d = messages[0].data
    d = d[2:]
    v = bytes_to_int(d) / 1.0
    return v * Unit.celsius

oil_temperature = OBDCommand("Engine oil temperature", 
"oil temperature", b"015C", 1, oil_temp, ECU.ALL,  False)

connection.supported_commands.add(oil_temperature)
while True:
    response = connection.query(oil_temperature)
    print(response.value)
    time.sleep(1)