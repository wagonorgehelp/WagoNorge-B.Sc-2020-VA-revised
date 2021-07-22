# The cloud server

## Installation on a Google Cloud server
Prerequisites:
 - Set up a google account.
 - "Enable the Compute Engine API"	

https://cloud.google.com/ 

Console -> Go to compute engine

### Initiate the cloud server
 1. VM instances -> Create instance.
 2. Bellow "Boot disk", click "Change" to configure the boot disk. 
 3. Bellow Public Images:
	- Operating system: Ubuntu 
	- Version: Ubuntu 18.04 LTS
	- Click "select" to confirm
 4. Bellow Firewall, choose:
	- "Allow HTTP traffic" 
	- "Allow HTTPS traffic" 
 5. Consider choosing a location with a close proximaty for less latancy. 
 6. Click Create to create the instance. 

The cloud server should now be set up with Linux Ubuntu as the operating system. 

### Installing Docker on an Ubuntu machine
Ref: https://docs.docker.com/engine/install/ubuntu/

Connect to the instance by clicking SSH under connect. 

1. Uninstall any older versions: 
```
sudo apt-get remove docker docker-engine docker.io containerd runc
``` 

 2. Update apt-package indeks:
```
sudo apt-get update
```
 3. Install packages to allow "apt" to use a repository over HTTPS:
```
sudo apt-get install \
apt-transport-https \
ca-certificates \
curl \
gnupg \
lsb-release
```
 4. Add Docker's official GPG kkey:
```
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
 5. Use the following command to setup a stable repository: 
```
 echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
 6. Install Docker Engine:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io
``` 

7. Verify the installation by running the following command:
```
sudo docker version
```

### Installing Docker-compose. 
Ref: https://docs.docker.com/compose/install/

 1. Download and install the last stable version of docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

 2. Add executable permission to the binary:
```
sudo chmod +x /usr/local/bin/docker-compose
```
 3. Verify that the installation was successfull by running this command:
```
sudo docker-compose --version
```

### Installing and setting up the server-scripts as Docker containers with docker-compose
 1. Download the docker-compose.yaml file. 
 	- It is available in this directory, and in the "Server Source Code.zip"-file as well.
 2. Upload the docker-compose.yaml file to the cloud server. 
  	- Can be done in the Google-SSH-client by clicking the settings-wheel and then "upload file"
 3. Run the following command:
```
sudo docker-compose up
``` 
Docker-compose automizes the installation and setup of the containers. 
 4. Give it a couple of minutes to download, install and setup.  


## Setting up the Grafana HMI

Grafana is available on: [server-ip]:3000

### Prerequisites
Download and unzip the "Server Source Code.zip"-file. 

### Log in:
 - Username: admin
 - Passord: admin

### Choose database
1. In the home menu, choose "Create a data source"
2. Search for MySQL, choose it and click "select".
3. Fill in the following:
	- Host: db:3306
 	- Database: processvalues
 	- User: root
 	- Password: example
4. Activate "Default"
5. Click "Save and Test" to save and test the communication. 


### Add the dashboard
1. Click the "+"-symbole (create) and choose "import". 
2. Click "Upload .json file".
3. Choose the "grafanadahsboard.json"-file. You will find it in Server Source Code -> LeakDetection
4. Click import. 
5. Click "Save dashboard" in the upper right corner and then "save" to save the dashbordet. 



## Using Adminer to access theMySQL database

1. Use your browser to connect to [server-ip]:8080
 	- Username: root
 	- Password: example
	- Database: *leave this blank*

2. Click log inn

Here you can brows the MySQL database, change things and read values. 

## Monitoring the HiveMQ MQTT-broker

By using the MQTT Websocket Client:

http://www.hivemq.com/demos/websocket-client/

1. Connect to the broker:
 	- Host: broker.hivemq.com
 	- Port: 8000
 	- Click "connect"

2. Subscribe to subjects


From the PLCs:
```
ba/wago/opcua/plc1/plcsub
ba/wago/opcua/plc2/plcsub
ba/wago/opcua/plc3/plcsub
ba/wago/opcua/plc1/plcpub
ba/wago/opcua/plc2/plcpub
ba/wago/opcua/plc3/plcpub
```
Simulation program information:

```
ba/wago/sim/info 
```

Weather from python to HMI:

```
ba/wago/sim/hmi/hmisub 
```
