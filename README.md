# Simple provider for control climate conditioner in daichi cloud

The implementation is written using open information obtained through open repositories and web sites
I don't have a goal to benefit from this software solution.

### TODO Function
[] filter by buildings 
[] filter by devices

## Features

- Control general parameters like fans speed, mode, temperature, etc
- Discovery devices and publish to MQTT
- Receive commands Homeassistant from MQTT and execute by API

## How to use

1. Copy .env.example and set value
2. run main.py

## For local development

1. docker-compose up -d
2. open http://localhost:2000
    3. user admin@example.com pass password123
    4. create client account user=admin, password=admin
3. brew install mqttui
4. read mqttui -b mqtt://localhost:1900 --username admin --password admin
5. publish mqttui -b mqtt://localhost:1900 --username admin --password admin publish test 23

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
  cr.yandex/crpt6a9sphouc986n0ji/homeassistant-daichi-cloud-climate-provider:20250822
````