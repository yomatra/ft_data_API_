# Studien_Projekt_Fischertechnik API

## Overview

This project consists of two main components:

* a Fischertechnik AI Quality Control Station with a TXT Controller
* a Raspberry Pi 

The system automatically captures an image of a product, evaluates it using an AI model, stores the result in a database, and sends the required control commands back to the Fischertechnik station.

## Raspberry Pi Services

The Raspberry Pi provides the central processing and communication platform. It runs:

* Arch Linux
* an MQTT broker
* the AI quality control application
* a database
* a REST API

The AI application and the API are started automatically during system boot.

## Process Flow

1. A product is placed on the Fischertechnik station.
2. The station captures an image of the product.
3. The image data is sent to the Raspberry Pi via MQTT.
4. The AI model processes the image and determines the quality result.
5. The Raspberry Pi sends the corresponding control command back to the TXT Controller.
6. The station transports or sorts the product.
7. The inspection result is stored in the database.
8. The stored data can be accessed through the API.

## System Start

1. Power on the Raspberry Pi.
2. Wait until the MQTT broker, API, database, and AI application are available.
3. Power on the Fischertechnik station and the TXT Controller.
4. Start the control program on the TXT Controller.
5. Place a product on the station to begin the inspection process.

## API

The API provides access to the stored inspection results.

```text
- API: http://IoT-Proj-Team-MGFCS.local:8000
- Swagger UI: http://IoT-Proj-Team-MGFCS.local:8000/docs
- OpenAPI JSON: http://IoT-Proj-Team-MGFCS.local:8000/openapi.json
- Health: http://IoT-Proj-Team-MGFCS.local:8000/health
```

## Requirements

* Raspberry Pi 
* Fischertechnik AI Quality Control Station
* TXT Controller
* Network connection between both systems (Raspberry Pi Lab)
* MQTT communication





# Standalone Conveyor Belt Inspection Dummy API

This is a small one-file API for local integration testing. It contains only
the dummy routes and dummy data, without database code or the main project
package.

## Run

```bash
pip install -r requirements.txt
uvicorn dummy_api:app --reload
```

Open:

- API: http://10.215.255.19:8000
- Swagger UI: http://10.215.255.19:8000/docs
- OpenAPI JSON: http://10.215.255.19:8000/openapi.json
- Health: http://10.215.255.19:8000/health

## Routes

- `GET /health`
- `GET /current_part`
- `GET /parts/last?limit=10`
- `GET /parts/since?timestamp=2026-05-31T08:01:03Z`
- `GET /parts/{part_id}`
- `GET /pictures?limit=10`
- `GET /parts/{part_id}/picture`
- `GET /groups`
- `GET /parts/{part_id}/group`
- `GET /parts/{part_id}/state`
