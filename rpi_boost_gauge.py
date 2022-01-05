import obd
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int

connection = obd.OBD()

def boost(messages):
    """decoder for boost messages"""
    d = messages[0].data
    d = d[1:]
    v = bytes_to_int(d) / 3.0
    return v * Unit.Turbocharger 

boost_pressure = OBDCommand("Turbocharger compressor inlet pressure",
"Turbo pressure", b"016F", 3, boost, ECU.ALL, True)

connection.supported_commands.add(boost_pressure)
response = connection.query(boost_pressure)
print(response.value)