# OPCUA-MQTT-link setup and installation

## Prerequisites
- All devices has the corresponding e!Cockpit program installed and running. 
- All devices has the CoDeSys OPC UA server installed. 
- All devices has Docker installed. 
- An SSH client.
- Internet connection on the device. 
- A local OPCUA-client. Recommeded: UAExpert. 
- An account on the Docker-hub https://hub.docker.com/
- Docker Desktop installed locally on your computer, with the setup complete and docker running. 
- Git Bash (or something similar) installed locally to access local Docker commands on your computer.

Recommended
 - Visual Studio Code or Notepad++ for editing files

## Setup 
NB! For external users: within the .bat executables and all dockerfiles. Please change the push/pull repository docker-hub destination to your own. Moreover, use another MQTT broker and/or change all used MQTT-topics within the setup-files and and python-scripts

The setup can be squashed if the .env's, .hmi, .plc1, .plc2, and .plc3 somehow matches your setup. 

### Notice
All used OPCUA-MQTT-Client images are built from "ImageTemplate". To change Python versions or libraries in the containers, modify the Dockerfile within "ImageTemplate" and then build and push it using the "push.bat" from the same folder. Then push the other images for changes to take effect. 


### Create a builx builder 
Required to push images to docker-hub, since the files are too large to be built on the device
1. Open Git bash.
2. Add builder by copy pasting the commands
```
docker buildx create --name builder-for-plc
```
3. Configure to use it
```
docker buildx use builder-for-plc
```

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

9. Save the .env file. Perhaps copy the contents to the .hmi file as a backup.
10. Open the "push.bat"-file, make sure that your own and the correct docker-hub repository is selected (before "--push"). Save and close. 
11. Build and push the docker image, with all the files in this folder, by double-clicking the "push.bat"-file. Verify that it pushed correctly by checking the Docker Hub. 

### Setting up the PLCs
This process is repeated for all 3 PLCs. For simplicity, start with PLC1. 
 1.  Gather the NodeId string for PLCX by connecting to the OPCUA server with UAExpert for example.  
 2.  Repeat the same process, only this time change the .plcx (e.g.: .plc1) in the PLC folder.
 3.  Once you are ready to push the image with the changes. Copy the contents of the .plsx-file, and paste it to the .env files. Save both files.
 4.  Then double-click the plsx.bat file corresponding to the plc (e.g.: plc1.bat).
 5.  Repeat for plc 2 and plc 3. 


## Installation
Access the device through an SSH terminal (PuTTY for example). 
1. Download and install the docker image corresponding to the device. By executing one of the commands.

```
docker pull wagonorge/opcua-mqtt-link-hmi
```
```
docker pull wagonorge/opcua-mqtt-link-plc1
```
```
docker pull wagonorge/opcua-mqtt-link-plc2
```
```
docker pull wagonorge/opcua-mqtt-link-plc3
```
2. Pulling the repository may take some time. Once it is done, initiate the container by running the corresponding command.
```
docker run -d --restart always -p 9999:9999 --name client wagonorge/opcua-mqtt-link-hmi
```
```
docker run -d --restart always -p 9999:9999 --name client wagonorge/opcua-mqtt-link-plc1
```
```
docker run -d --restart always -p 9999:9999 --name client wagonorge/opcua-mqtt-link-plc2
```
```
docker run -d --restart always -p 9999:9999 --name client wagonorge/opcua-mqtt-link-plc3
```
3. Verirfy that the container runs correctly by checking the log.
```
docker attach client
```
There should not be any errors or tracebacks. 

# Changelog 

## 20.07.2021 
### Template dockerfile
- Fixed "cryptography is not defined" by implementing the following actions in the dockerfile. 
  - updating pip installer to the latest version.
  - Specifically installing cryptography version 3.1.1

### Main python program and .env setups
- Removed unnecessary items from the .env file, and changed how NodeId is generated in all "`\__main__.py" scripts to ease setup and installation. 
