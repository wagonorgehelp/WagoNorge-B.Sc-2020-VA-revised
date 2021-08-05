# WagoNorge-B.Sc-2020-VA-demo

## Info
This repository contains a revised version of a bachelor written for Wago Norge, the spring of 2020.  

Credits to the original authors: 
- Johan Haukalid
- Markus Raudberget
- Jone Vassbø 
- Peder Ward

Original repository https://github.com/Wago-Norge/Bachelorprosjekt-2020 (Curtain aspects are obsolete, missing installation steps and fixes are presented in this repository)

![VA-systemExplenation](https://user-images.githubusercontent.com/61655489/128310474-869abdb6-823f-4f6d-846c-a04802752f17.PNG)




### Contents
- A detailed installation guide
- Fixed incompatibility issues. Running fine 07.2021
- A few program adjustments that eases the installation

### Program functionalities and contents
- PLCs and HMI
    - e!cockpit program that simulates input output and measurements.
    - A docker container that ports values from the PLCs OPC UA server to an MQTT broker. The container contains a python script that uses the "freeopcua"-library as the OPCUA-client and the "paho-mqtt"-library as the MQTT client.
- Cloud server:
    - Hosts a Grafana visualization. 
    - Simulation
    - Leak Detection
    - Observes the PLCs
## Requirements
- 3x Wago PFC200 PLCs
- A Wago TP600 PIO3 touch panel
- A Google-cloud server (or optionally a computer that can host the cloud-server locally).
- An MQTT-broker

## Installation

Follow the README.md within "PLC-side" for PLC installations, and "Server-side" for server installations

## Communication overview

### Network topology

![nettverkstopologi](https://user-images.githubusercontent.com/73703856/126310533-434e2935-3811-43e7-9c68-7a60520869a0.PNG)

### Between PLC and HMI
![complchmi](https://user-images.githubusercontent.com/73703856/126310704-1504c6b8-5a10-4e38-9215-10343fc181ba.PNG)

### Between PLC and cloud server
![complccloud](https://user-images.githubusercontent.com/73703856/126310799-a78a4a43-2fe5-411f-b26d-0f1074661bec.PNG)

### Network topology (locally configured with edge computer)
![Nettverkstopologi](https://user-images.githubusercontent.com/61655489/127852940-8ea0943c-2112-4dc3-886e-c81af2653c64.png)


