
# Using an Edge-computer as the cloud server and MQTT-broker
Instead of hosting the cloud-server externally on a 3rd-party server, it could also run locally like for instance on an Edge-Computer.



## Tips
 - Instead of using an SSH-client like PuTTY, there is a terminal available on: [ip-address of the edge-computer]:9090

### Enable automatic boot on power up
By default, the Edge Computer will have to be manually turned on by operating the power-button (ATX-mode). For most intents and purposes it is practical that it boots automatically when the device has power(AT-mode). This can be done by setting two dipswitches on the motherboard within the Edge Computer. 

To find out how to do this, please download the Edge Computer manual (for [752-940x](https://www.wago.com/global/plcs-%E2%80%93-controllers/edge-computer/p/752-9400#downloads)).
CTRL + F and search "SW1" and you will find where the switches are located and how to set them. There should be two dipswitches, and they should be set to the opposite of their default setting. 

## Prerequisites
 - a Wago Edge-Computer
 - An internet connection

## Installing Docker and Docker Compose

### Installing Docker

Follow this guide [here](https://docs.docker.com/engine/install/debian/)

### Installing Docker Compose

Follow this guide [here](https://docs.docker.com/compose/install/)

## Installing the Docker containers
- Make sure that the servers MQTT-clients refers to the IP-adress of the edge-computer build and push the changes.

1. Transfer the "docker-compose.yaml"-file to the device using and FTP-capable service like FileZilla. 
2. Connect to the Edge Computer using an SSH-client, and navigate to the location of the "docker-compose.yaml"-file.
3. Make sure none of the relevant docker images allready exists on the device, if so remove them to make sure that the latest images are downloaded (docker-compose will not pull an image if it exists on the device).
4. Run the following command:
```
docker-compose up
```


## Setting up the MQTT Broker

[Links to docker hub repository](https://hub.docker.com/_/eclipse-mosquitto)

Eclipse Mosquitto provides an MQTT-broker that can run on the device as a Docker Container. Installation is included with the docker-compose file. 
As of Mosquitto MQTT version > 2.0.0, it defaults to "local only mode", it is a security feature that ensures that the MQTT-broker only operates locally if nothing else is specified. To enable external communication, we have to include a port listener to the broker in the configuration file. 

### Installation using docker-compose
Either transfer the "docker-compose.yaml"-file from this directory to the edge-computerl, using a FTP-capable service like FileZilla, or pull the "eclipse-mosquito" image manually from the Docker-hub using regular Docker commands.



### Installation without docker-compose
1. Pulling the image from the docker-hub. 
```
docker pull eclipse-mosquito 
```
2. Initiate the container
``` 
docker run -d --restart always -p 1883:1883 -p 9001:9001 --name mqtt eclipse-mosquitto
```

### Setup
Note: make sure that the Docker-container is running: 
```
docker ps -a
```

1. Access the container
```
docker exec -ti mqtt /bin/sh
```
2. Open the mosquitto.conf-file
```
vi /mosquitto/config/mosquitto.conf
``` 
3. Press "i" to enter edit-mode. Then add the following to the config file
``` 
persistence true
persistence_location /mosquitto/data/
allow_anonymous true
listener 1883
``` 
4. Press "ESC" to exit edit mode.
5. Then type ":wq" to write(save) and quit.
6. Type the command "return" to exit the container. 
7. Restart the container.
```
docker restart mqtt
```
8. Clients should now be able to connect. Verify by checking the container log
```
docker attach mqtt
```
or
```
docker logs mqtt -f
```
(ctrl + c to stop viewing the log)

## Setting up the MQTT-clients for the new MQTT-broker
As we are going to use a different MQTT-broker, it is important to change the MQTT addressing for all MQTT-clients.

### Setup for the cloud-server MQTT-clients

Open up the following Python scripts and reffer to the following lines. 
 - DataStore -> mqtt_to_mysql.py (line 16)
 - SimulationProgram -> \__main__.py (line 23)

Make sure that "mqttBroker" is set to the IP-address of the Edge-computer. 

e.g.
```
mqttBroker = "192.168.10.150"
``` 

Push the new changes to the docker-hub by using the push.bat (make sure that docker is running with a builx builder running as well. How to do this is covered in the PLS-side setup readme. Make sure that your own docker-repository is set up within the push.bat files. 

Use the docker-compose functionality (as used for the Google-cloud installating) to install the changed docker containers. 

### WBM setup for all devices
Make sure that within the Web Based Management for HMI, PLC1, PLC2 and PLC3 that the Hostname for the MQTT cloud connection is set to the IP of the edge-computer and not "broker.hivemq.com".

### Setup for the PLCs MQTT-clients
Within the .env for all 4 devices' "OPCUA_MQTT_link" container, make sure that "MQTT_BROKER" is set to the IP-address of the edge-computer.

e.g.:
```
MQTT_BROKER=192.168.10.150
```

Push the images to the docker-hub. Pull and run them the same way as covered in PLS-side setup readme. 

