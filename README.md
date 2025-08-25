# Control air conditioner in daichi cloud for homeassistant

The implementation is written using open information obtained through open repositories and web sites
I don't have a goal to benefit from this software solution.

## Features

- [x] Control general parameters like fans speed, mode, temperature, etc
- [x] Discovery devices and publish to MQTT
- [x] Receive commands Homeassistant from MQTT and execute by API
- [x] Enable silent mode
- [] filter by buildings and devices
- [] enable discovery interval setup
- [] order of command and check result

## How to use from source

1. Copy .env.example and set value
1. DAICHI_USER=user@example.net # you username in https://web.daichicloud.ru
1. DAICHI_PASS=password1 # you password in https://web.daichicloud.ru
1. MQTT_HOST=localhost # home assistant mqtt host
1. MQTT_PORT=1883 # home assistant mqtt port 
1. MQTT_USER=admin # home assistant mqtt user
1. MQTT_PASS=admin # home assistant mqtt pass
1. APP_ENABLE_MUTE_SOUND=True # enable or disable silent mode
1. Install Python 3.12
1. Install requirements `pip install -r requirements.txt`
1. `python main.py`

## How to use by docker

### Docker Hub
https://hub.docker.com/repository/docker/alfss/homeassistant-daichi-cloud-climate-provider

### docker-compose
Create docker-compose.yml file and .env file

````
version: '3.8'
services:
  daichi-cloud-climate:
    image: alfss/homeassistant-daichi-cloud-climate-provider:v1.0.1
    env_file:
      - .env
    restart: unless-stopped
````

## MQTT Topics
Command = daichi_cloud_climate/device_id_{ID}/ac/+
Discovery = homeassistant/climate/daichi_cloud_{ID}/climate/config

## For local development

1. docker-compose up -d
2. open http://localhost:2000
    3. user admin@example.com pass password123
    4. create client account user=admin, password=admin
3. brew install mqttui
4. read mqttui -b mqtt://localhost:1900 --username admin --password admin
5. publish mqttui -b mqtt://localhost:1900 --username admin --password admin publish test 23

## For docker.io login
```
docker login docker.io
```
Release steps
```shell
make build_for_public
make print_tag
make publish_public
```
## How to run in docker

````bash
docker run --rm \                                                                                                                             1 ↵
  -e DAICHI_USER='user@domain.net' \
  -e DAICHI_PASS='you_passwotd' \
  -e MQTT_HOST="MQTT-host" \
  -e MQTT_PORT="1900" \
  -e MQTT_USER="admin" \
  -e MQTT_PASS="admin" \
  -e APP_ENABLE_MUTE_SOUND="True" \
  alfss/homeassistant-daichi-cloud-climate-provider:v1.0.1
````