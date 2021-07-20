cp .hmi .env
cd ..
cd ..
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -f OPCUA_MQTT_link/HMI/Dockerfile -t wagonorge/opcua-mqtt-link-hmi --push .