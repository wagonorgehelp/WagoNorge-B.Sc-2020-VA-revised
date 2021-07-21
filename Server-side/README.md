# The cloud server

## Installation on a Google Cloud server
Prerequisites:
 - Set up a google account.
 - "Enable the Compute Engine API"	

https://cloud.google.com/ 

Console -> Go to compute engine

### Initiate the cloud server
 1. VM instances -> Create instance.
 2. Under Boot disk, klikk Change for å konfigurere boot disken. 
 3. Under Public Images:
	- Operating system: Ubuntu 
	- Version: Ubuntu 18.04 LTS
	- Klikk deretter select for å bekrefte. 
 4. Under Firewall, velg:
	- "Allow HTTP traffic" 
	- "Allow HTTPS traffic" 
 5. Vurder å velge en region i Europa (Nederland f.eks.).
 6. Klikk Create for å lage instansen. 

### Installere Docker i skyserveren
Ref: https://docs.docker.com/engine/install/ubuntu/

Koble deg til instansen ved å trykke SSH under connect

 0. Avinstaller eldre versjoner:
```
sudo apt-get remove docker docker-engine docker.io containerd runc
``` 

 1. Oppdatere "apt"-pakke indeks:
```
sudo apt-get update
```
 2. Installere pakker for at apt kan bruke repository over HTTPS (Ved melding: skriv "Y" og trykke enter, ignorer evt. error):
```
sudo apt-get install \
apt-transport-https \
ca-certificates \
curl \
gnupg \
lsb-release
```
 3. Legge til Dockers offisielle GPG nøkkel:
```
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
 4. Bruk følgende kommando for å sette opp stable repository: 
```
 echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
 5. Installere Docker Engine:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io
``` 

6. Verifiser at det er installert riktig, ved å kjøre:
```
sudo docker version
```

## Installere Docker-compose. 
Ref: https://docs.docker.com/compose/install/

 1. Laste ned siste stabile versjon av docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

 2. Legge til kjørerettigheter til binary:
```
sudo chmod +x /usr/local/bin/docker-compose
```
 3. Verifiser at det er installert riktig ved å kjøre følgende kommando.
```
sudo docker-compose --version
```

# Installere images
 1. Flytt over docker-compose.yaml filen. 
   - Kan gjøres i SSH-klienten til Google, ved å trykke på instillinger/hjulet øverst til høyre, så "upload file"
 2. Kjør:
```
sudo docker-compose up
``` 
Den automatiserer installasjon og oppsett
 3. Gi den noen minutter på laste ned, installere og start opp. 

"docker-compose.yaml" filen kan inneholde følgende:
```
version: "3.1"

services:
  mqtttomysql:
    image: jonev/mqtt-mysql-store
    depends_on:
      - db

  simulation:
    image: jonev/water-simulator
    depends_on:
      - db

  leakdetection:
    image: jonev/leak-detection
    depends_on:
      - db
      - simulation

  grafana:
    image: jonev/grafana-with-plugins
    ports:
      - 3000:3000
    depends_on:
      - db

  db:
    image: mysql
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_ROOT_PASSWORD: example
  adminer:
    image: adminer
    ports:
      - 8080:8080
    depends_on:
      - db
  portainer:
    image: portainer/portainer
    command: -H unix:///var/run/Docker.sock
    restart: always
    ports:
      - 9000:9000
      - 8000:8000
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
volumes:
  portainer_data:

```

# Sette opp Grafana HMI

Grafana er tilgjengelig på: [ip-adresse]:3000

### Forarbeid
Last ned og unzip kildekode zipfilen. Den er tilgjengelig på linken under

https://github.com/Wago-Norge/Bachelorprosjekt-2020/blob/master/Dokumentasjon%20og%20Kildekode/Open%20Source%20kode_v1.0.0.zip


### Logg inn:
 - Brukernavn: admin
 - Passord: admin

### Velge database
1. På Hjem/home menyen, velg "Create a data source"
2. Søk etter MySQL, velg den og trykk "select".
3. Fyll inn følgende:
 - Host: db:3306
 - Database: processvalues
 - User: root
 - Password: example
4. Aktiver "Default"
5. Trykk så "Save and Test" for å lagre og sjekke kommunikasjonen. 


### Legge til ferdig dashboard
1. Trykk på "+"-symbolet (create) og velg import. 
2. Trykk så "Upload .json file".
3. Velg "grafanadahsboard.json". Den finner du i "Open Source kode"-mappen du lastet ned: drinking-water-distri... -> LeakDetection
4. Trykk så import. 
5. Trykk så "Save dashboard" øverst i høyre hjørne, også "save" for å lagre dashbordet. 





# Bruke Adminer til å få tilgang til MySQL databasen

1. Bruk en nettleser til å koble til [ip-adresse]:8080
 - Brukernavn: root
 - Passord: example
 - Database: *ikke skriv noe her*

2. Klikk Logg inn

# Monitorere HiveMQ MQTT-brokeren

Ved å benytte MQTT Websocket Client:

http://www.hivemq.com/demos/websocket-client/

1. Koble deg til brokeren:
 - Host: broker.hivemq.com
 - Port: 8000
 - Trykk "connect"

2. Abonner på emner:

Emner man kan abonnere på:


       ba/wago/opcua/plc1/plcsub
       ba/wago/opcua/plc2/plcsub
       ba/wago/opcua/plc3/plcsub
       ba/wago/opcua/plc1/plcpub
       ba/wago/opcua/plc2/plcpub
       ba/wago/opcua/plc3/plcpub


