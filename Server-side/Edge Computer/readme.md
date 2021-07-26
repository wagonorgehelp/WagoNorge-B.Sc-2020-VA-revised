
# Using an Edge-computer as the cloud server and MQTT-broker

## Prerequisites
 - Docker installed on the Edge-computer
 - Docker-compose installed on the edge computer

## Setting up the devices for the new MQTT-broker
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

Push the new changes to the docker-hub by using the push.bat (make sure that docker is running with a builx builder running as well. How to do this is covered in the PLS-side setup readme). Make sure that your own docker-repository is set up within the push.bat files. 

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
## Setting up the MQTT Broker

https://hub.docker.com/_/eclipse-mosquitto

Eclipse Mosquitto provides an MQTT-broker that can run on the device as a Docker Container. Installation is included with the docker-compose file. 
As of Mosquitto MQTT version > 2.0.0, it defaults to "local mode", meaning that the server is only available locally on the machine. To enable external communication, we have to include a port listener to the broker in the configuration file. 

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
4. Press "ESC" to exit enter mode.
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

## Changes PLC-side mqtt-client

Change the .env's in OPCUA-MQTT-link for HMI and PLCs

Change the cloud connectivity settings in all devices. 
