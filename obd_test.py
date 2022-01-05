import obd

connection = obd.OBD(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 


cmd= obd.commands.RPM

response = connection.query(cmd)

print(response.value) 
