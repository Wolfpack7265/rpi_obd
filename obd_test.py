import obd 

ports = obd.scan_serial()                         
connection = obd.OBD(ports[0])

cmd= obd.commands.SPEED

response = connection.query(cmd)

print(response.value) 
