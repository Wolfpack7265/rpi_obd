# rpi_boost_gauge

Introduction 

Objectives
First prototype: >>>>> done 
-connect to an OBD2 port using an ELM327 module and Bluetooth built into a raspberry pi >>>>> done 
    -done at first through an ELM327 emulator for windows 
-analyze and manipulate data from the car's ECU (emulator) >>>>> done
-create a GUI to display data >>>>> done
-create launcher.sh shell file to consolidate launch tasks of the program >>>>> done 
-connect to a car's ECU for the first time >>>>>done 
    -bluetooth connection needs to be binded to an RF com port (/dev/rfcomm0)
-prevent display from entering sleep shutoff >>>>> done 
-automate launching of the program on startup(/lib/systemd/system/obd.service) >>>>>done 
-automate bluetooth connection >>>>>done 

Second Prototype:
-re-write obd with obd.async instead of obd.OBD()
    -remove obd.OBD commands, as they act as stop commands
    -reduce lag for data query 
-integrate touchscreen interface library (configurable settings)
-add more measurements (gas mileage, rpm, coolant temperature, etc.)
-add acceleration metrics(0-100 times, G-force?, etc.)

Future Iterations:
-track-focused unit?
    -larger rectangular screen
    -raspberry pi 4 
    -video recording? 
    -data logging (vs. instant data of 1st and 2nd iteration)
-dashcam integration?
    -raspberry pi 5MP or 8MP camera module
Hardware  



