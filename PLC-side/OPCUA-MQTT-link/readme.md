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

### Setting up the client for the HMI
1. Connect to the OPCUA server on the HMI-device using an OPCUA-client (UAExpert is used in this example). 
2. Within the HMI folder, open the .env in an editor. 
3. 

## Installation



# Changelog 

## Template dockerfile

## Main python program and .env setups
