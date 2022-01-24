# rpi_obd

Introduction 

Objectives
First prototype: >>>>> done 
-connect to an OBD2 port using an ELM327 module and Bluetooth built into a raspberry pi >>>>> done 
    -done at first through an ELM327 emulator for windows 
-analyze and manipulate data from the car's ECU (emulator) >>>>> done
-create a GUI to display data >>>>> done
-create launcher.sh shell file to consolidate launch tasks of the program >>>>> done 
-connect to a car's ECU for the first time >>>>>done 
    -uses bluetoothctl to connect MAC address of ELM327 module
    -bluetooth connection needs to be binded to an RF com port (/dev/rfcomm0)
-prevent display from entering sleep shutoff >>>>> done 
-automate launching of the program on startup(/lib/systemd/system/obd.service) >>>>>done 
-automate bluetooth connection >>>>>done 
    -done through launcher.sh file, writes bluetoothctl command lines before launching the python script 

The purpose of the initial prototype was to develop various parts of the project for basic functionality; This includes prototyping and packaging the hardware, developing the CAD files, and producing the code that will be used to establish connection to a car's ECU. At this stage, a GUI was developed to visualize data, and the raspberry pi os was experimented on to automate bluetooth connections and run without user input. This stage of the design is meant to be a functional proof-of-concept design, but still have plenty of room for optimization and improvement. 

Second Prototype:
-re-write obd with obd.async instead of obd.OBD()
    -remove obd.OBD commands, as they act as stop commands
    -reduce lag for data query 
    -refresh fps goal: 30fps 
-integrate touchscreen interface library (configurable settings)
-add more measurements (gas mileage, rpm, coolant temperature, etc.)
-add acceleration metrics(0-100 times, G-force?, etc.)

The second stage prototype aims to improve aspects of the original, specifically to the python script. The main goal is to heavily optimize the refresh rate of receiving data, and generally reduce redundancies. The python script will be re-written to incorporate obd.async, to improve the performance of UI elements. The optimization of the code will also allow for easier implementation of additional features, including: touchscreen integration, configurable settings and additional calculations from ECU readings. In terms of hardware, minor tweaks will be made to CAD files to improve the fit of components, and a new main casing will be 3D-printed in PETG for increased heat resistence.

Future Iterations:
-track-focused unit?
    -larger rectangular screen
    -raspberry pi 4 
    -video recording? 
    -data logging (vs. instant data of 1st and 2nd iteration)
-dashcam integration?
    -raspberry pi 5MP or 8MP camera module

Future plans for this project include a companion product: a "track-focused" version of the device that would be more focused on data-logging instead of displaying only instant data from the ECU. 

Hardware  


