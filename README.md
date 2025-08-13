# Simple provider for control climate conditioner in daichi cloud
The implementation is written using open information obtained through open repositories and web sites
I don't have a goal to benefit from this software solution.

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