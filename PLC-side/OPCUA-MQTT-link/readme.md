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
NB! For external users: within the .bat executables and all dockerfiles. Please change the push/pull repository docker-hub destination to your own. Moreover, use another MQTT broker or change all used MQTT-topics within the setup-files and and python-scripts

This step can be squashed if the .env's, .hmi, .plc1, .plc2, and .plc3 somehow matches your setup. 
- Download and unpack "OPCUA_MQTT_link.zip"

### Setting up the client for the HMI-device
1. Connect to the OPCUA server on the HMI-device using an OPCUA-client (UAExpert is used in this example). 
2. Within the HMI folder, open the .env in an editor. 
3. Within UAExpert, in Address Space, navigate Root -> Objects -> DeviceSet -> TP 600... -> Application -> GlobalVars -> HMI.
4. Click on any variable marked with a green label. 
5. Node information should be available in the "Attributes" tab on the right-hand side. 
6. Doble click on the "Identifier" value within "NodeId". Copy and paste the identifier string to notepad or something like that. It should look something like this: 
```
|var|TP 600 7.0 800x480 PIO3 CP.Application.HMI.AliveCounterPlc1Pv
```
7. Now crossreference this with the contents of the .env file:
```
WAIT_TIME=1
OPC_UA_SERVER=172.17.0.1
OPC_UA_SERVER_USERNAME=admin
OPC_UA_SERVER_PASSWORD=wago
OPC_UA_ID=TP 600 7.0 800x480 PIO3 CP
OPC_UA_APP=Application
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
MQTT_PUBLISH_PV_SUFFIX=Pv
```
8. Chang it accordingly
  - "OPC_UA_SERVER" OPC UA client end-point IP is currently set to localhost (172.17.0.1)
  - "OPC_UA_ID" should contain what every is after "|var|" until the first "." in step 6.
  - "OPC_UA_APP" should contain what ever is after the first "." until the next. 
  - "MQTT_BROKER" should contain the URL of your desidered MQTT broker. 
  - "MQTT_PORT" should contain the port of your desired MQTT broker. 
  - "MQTT_PUBLISH_Pv_SUFFIX" leave unchanged. 


## Installation



# Changelog 

## Template dockerfile

## Main python program and .env setups
