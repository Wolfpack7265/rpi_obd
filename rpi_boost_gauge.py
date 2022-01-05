import obd
import time
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int
loop = True
connection = obd.OBD(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 

def boost(messages):
    """decoder for boost messages"""
    d = messages[0].data
    d = d[2:]
    v = bytes_to_int(d) / 3.0
    return v 

boost_pressure = OBDCommand("Turbocharger compressor inlet pressure",
"Turbo pressure", b"016F", 3, boost, ECU.ALL, True)

connection.supported_commands.add(boost_pressure)
while True:
    response = connection.query(boost_pressure)
    print(response.value)
    time.sleep(1)