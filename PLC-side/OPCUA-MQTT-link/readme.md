# OPCUA-MQTT-link setup and installation

## Prerequisites
- All devices has the corresponding e!Cockpit program installed and running. 
- All devices has the CoDeSys OPC UA server installed. 
- All devices has Docker installed. 
- An SSH client.
- Internet connection on the device. 
- A local OPCUA-cient. Recommeded: UAExpert. 

Recommended:
 - Docker Desktop installed locally on your computer.
 - Visual Studio Code or Notepad++ for editing files

## Setup 
NB! For external users: within the .bat executables and all dockerfiles. Please change the push/pull repository docker-hub destination to your own. 

This step can be squashed if the .env's, .hmi, .plc1, .plc2, and .plc3 somehow matches your setup. 
- Download and unpack "OPCUA_MQTT_link.zip"

### Setting up the client for the HMI-device
1. Connect to the OPCUA server on the HMI-device using an OPCUA-client (UAExpert is used in this example). 
2. Within the HMI folder, open the .env in an editor. 
3. Within UAExpert, in Address Space, navigate Root -> Objects -> DeviceSet -> TP 600... -> Application -> GlobalVars -> HMI.
4. Click on any variable marked with a green label. 
5. Node information should be available in the "Attributes" tab on the right-hand side. 
6. Doble click on the "Identifier" value within "NodeId". Copy and paste the identifier string to a clipboard. It may look something like this: 
'''txt
|var|TP 600 7.0 800x480 PIO3 CP.Application.HMI.AliveCounterPlc1Pv
'''

## Installation



# Changelog 

## Template dockerfile

## Main python program and .env setups
