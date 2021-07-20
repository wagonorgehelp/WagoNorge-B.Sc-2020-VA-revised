# Installing the e!cockpit programs

Last verified firmware version: FW18

### Prerequisites
- Perform a firmware update, or confirm that you have the latest available firmware installed.
- Make sure all PLCs are set up with internet access.  

## Setup in Web Based Management
Access the the WBM for the appropiate Wago device, and repeat the process for all 4 devices

### Settings
 1. Configuration -> Networking -> TCP/IP Configuration
    - Make sure that the PLC has a static IP-address setup in the range of the router in the LAN. 
    - Manually assign a custom DNS Server: e.g. 8.8.8.8
 2. Networking -> Routing 
    - Enable "IP Forwarding through multiple interfaces"
    - Setup a Default static route that corresponds with the router in the LAN. 
 3. Clock
    - Make sure that the local time and date matches/is close to the real local time and date. 
 4. Pors and Services -> Network Services
    - Just enable everything. 
 5. ... -> PLC Runtime Services
    - CODESYS 2: enable webserver and communication. 
    - e!RUNTIME: enable webserver. 


### Installing CoDeSys OPC UA Server
Wagos own OPC UA Server does no longer support the setup of multiple node IDs for structures and arrays. Therefore, for the OPCUA-MQTT-link to work properly, the CoDeSys OPC UA server needs to be installed via an IPK. 

1. Download the IPK: https://wago.sharefile.eu/share/view/s311dc640445b497cb356dbc9fb4b20b5
2. Unpack/unzip it.
3. In WBM: Configuration -> software Uploads. 
4. Wait a couple of minutes for the software to install. 
5. Verify the installation by going to Fieldbus -> OPCUA. There should now, only be a single option available. 

### Install Docker-ipk
The OPCUA-MQTT-link runs as a Docker-container. Therefore 



## Setup in e!Cockpit

