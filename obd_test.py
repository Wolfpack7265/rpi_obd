import obd
loop = True
connection = obd.OBD(portstr="COM4", baudrate="38400", protocol=None, fast=True, timeout=0.1, check_voltage=True, start_low_power=False) 

while True:
    cmd= obd.commands.COOLANT_TEMP

    response = connection.query(cmd)

    print(response.value) 
