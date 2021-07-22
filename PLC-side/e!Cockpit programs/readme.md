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
 6. Setup MQTT cloud connection. Cloud Connectivity -> Connection 1
    - Enabled: checked
    - Cloud Platform: MQTT AnyCloud
    - Hostname: broker.hivemq.com
    - Portnumber: 1883
    - Client ID (e.g.): WAGOPLC3
 7. Reboot the PLC

### Installing CoDeSys OPC UA Server
Wagos own OPC UA Server does no longer support the setup of multiple node IDs for structures and arrays. Therefore, for the OPCUA-MQTT-link to work, the CoDeSys OPC UA server needs to be installed via an IPK. 

1. Download the IPK: https://wago.sharefile.eu/share/view/s311dc640445b497cb356dbc9fb4b20b5
2. Unpack/unzip it.
3. In WBM: Configuration -> software Uploads. Upload the .ipk file. 
4. Wait a couple of minutes for the software to install. 
5. Verify the installation by going to Fieldbus -> OPCUA. There should now only be a single option available. 

### Install Docker-ipk
The OPCUA-MQTT-link runs as a Docker-container. Therefore docker needs to be installed on the device.

Follow this guide: https://github.com/WAGO/docker-ipk


## Setup in e!Cockpit
Repeat the process with the corresponding program for all 4 devices. 
For the HMI it is recommended to use a large TP600 PIO3 panel. It could also run on a PFC200 and the visualization be called through webvisu. 

### Download and setup
1. Dowload the e!Cockpit program. 
   - Option 1: Create a new project and import the .export files. 
   - Option 2: Download and run .ecp files. 
2. Set it up with your desired controller. Either by changing the PLC type. If this causes unfixable errors: Add your controller and copy-paste the contents from the original controller. (libraries should be manually installed.
3. Install the libraries (Library manager -> Add library).
   Required libraries:
   - CmpApp
   - CmpEventMgr
   - CmpIecTask
   - Component Manager
   - Standard
   - VisuDialogs
   - WagoAppCloud
   - WagoAppJSON
   - WagoAppString
   - WagoAppTime
 5. Make sure there is a "Symbol Configuration". Within it make sure "HMI" and "STATUS" is checkmarked along with all variables/structs underneath. 
 6. Rebuild the program and make sure that it runs without errors. Connect and download to the device. 

### Install visualization profile for HMI
For the HMI visualization to look correctly the vizualization profile needs to be installed.
1. Download "styledef.visustyle.xml"
2. In the vizualization profile, click the lightning bolt in the upper right corner of "Style Settings". 
3. Click open style editor. Then it takes a couple of seconds to boot. 
4. In Style Editor, click File -> Open and then select "styleddef.visustyle.xml" you just downloaded. 
5. Once it opens, remember the name, click File -> Save and install. 
6. Close Style Editor. 
7. Make sure that the installed style is selected under Style Settings -> Selected style. 


### Image pool in HMI
- Make sure the image pool "WAGO" is within the application and device-structure. 
- If not, download the "imagepool.export" and import it. 
