# IoT Vehicle Tracking & Theft Prevention System

## Project Overview

The **IoT Vehicle Tracking & Theft Prevention System** is an IoT-based security and monitoring project designed to track a vehicle’s real-time location using GPS coordinates and provide theft-prevention features such as geofencing, movement alerts, and remote engine lock/unlock control.

This project is suitable for students who want to build an industry-oriented IoT project using either real hardware or virtual simulation.

The system can be used to monitor:

* Vehicle latitude and longitude
* Vehicle speed
* Geofence status
* Theft alert status
* Engine lock/unlock status
* Location history logs
* Google Maps location links

This project supports both:

* Hardware implementation using ESP32 and GPS module
* Virtual simulation implementation using Python backend and web dashboard

---

## Problem Statement

Vehicle theft and unauthorized vehicle movement are common security issues. Many vehicle owners, logistics companies, delivery services, and school transport systems need a way to track vehicles in real time and receive alerts when a vehicle leaves a safe zone.

Manual tracking is not efficient because:

* Vehicle location cannot be monitored continuously
* Theft may not be detected immediately
* Route history may not be available
* Owners cannot remotely disable the vehicle
* Fleet operators cannot monitor movement from a dashboard

This project solves these problems by using GPS, IoT communication, geofencing, alert logic, and remote control.

---

## Objectives

The main objectives of this project are:

* Track vehicle location in real time
* Display latitude and longitude on dashboard
* Generate Google Maps location link
* Detect if vehicle leaves a predefined safe zone
* Generate theft alerts
* Store vehicle movement history
* Provide remote engine lock/unlock simulation
* Support virtual GPS simulation if hardware is not available
* Generate CSV/PDF reports
* Build a GitHub-ready proof-of-work IoT project

---

## Features

* Real-time GPS tracking
* Latitude and longitude display
* Speed monitoring
* Google Maps link generation
* Geofence detection
* Theft alert generation
* Engine lock/unlock control
* Virtual GPS movement simulation
* Location history logging
* CSV report download
* PDF report generation
* Dashboard visualization
* Manual vehicle reading input
* REST API backend
* Beginner-friendly project structure
* Suitable for academic and portfolio use

---

## IoT Concepts Used

This project demonstrates the following IoT concepts:

* GPS data collection
* Sensor/module integration
* ESP32 communication
* Cloud/LAN dashboard concept
* Real-time monitoring
* Geofencing
* Alert generation
* Remote control
* Actuator/relay simulation
* Data logging
* API-based dashboard integration

---

## System Workflow

```text
GPS Module / Virtual GPS
        ↓
ESP32 / Python Simulation
        ↓
Location Data Processing
        ↓
Geofence Checking
        ↓
Theft Detection Logic
        ↓
Alert Generation
        ↓
Dashboard Update
        ↓
Engine Lock / Unlock Control
        ↓
Location History Report
```

---

## Architecture

```text
+--------------------------+
| GPS Module / Simulator   |
|--------------------------|
| Latitude                 |
| Longitude                |
| Speed                    |
| Movement Status          |
+------------+-------------+
             |
             v
+--------------------------+
| ESP32 / Backend API      |
|--------------------------|
| Location Processing      |
| Geofence Calculation     |
| Theft Detection          |
| Alert Logic              |
+------------+-------------+
             |
             v
+--------------------------+
| Dashboard                |
|--------------------------|
| Live Location            |
| Google Maps Link         |
| Engine Lock/Unlock       |
| Alerts                   |
| Logs & Reports           |
+--------------------------+
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLite
* CSV logging
* PDF report generation
* Uvicorn

### Frontend

* React / Vite
* HTML
* CSS
* JavaScript
* Dashboard UI
* API integration

### Hardware / Simulation

* ESP32
* NEO-6M GPS Module
* Relay Module
* Buzzer
* LED
* Optional GSM Module
* Python-based virtual simulation

---

## Hardware Components

| Component         | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| ESP32             | Processes GPS data and sends it to dashboard/cloud     |
| NEO-6M GPS Module | Provides latitude, longitude, speed, and location data |
| Relay Module      | Simulates engine lock/unlock control                   |
| Buzzer            | Generates local theft alert                            |
| LED               | Shows status indication                                |
| GSM Module        | Optional SMS alert backup                              |
| Power Supply      | Powers ESP32 and modules                               |
| Dashboard         | Displays live location and alerts                      |

---

## Folder Structure

```text
IoT-Vehicle-Tracking-Theft-Prevention-System/
│
├── arduino_code/
│   └── vehicle_tracking_esp32.ino
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── database.db
│   └── README.md
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│
├── python_simulation/
│   └── gps_simulation.py
│
├── data/
│   └── location_logs.csv
│
├── outputs/
│   └── vehicle_report.pdf
│
├── images/
│   └── dashboard_screenshot.png
│
├── circuit_diagram/
│   └── circuit.png
│
├── reports/
│   └── project_report.md
│
├── docs/
│   └── setup_guide.md
│
├── README.md
└── .gitignore
```

---

## Backend Setup

### Step 1: Open PowerShell

Go to backend folder:

```powershell
cd "C:\Projects\IOT\Internet of Things - IoT Vehicle Tracking & Theft Prevention System\iot_vehicle_tracking_backend"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

### Step 4: Install Requirements

```powershell
pip install -r requirements.txt
```

### Step 5: Run Backend Server

```powershell
python -m uvicorn main:app --reload
```

### Step 6: Open API Documentation

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Open a new PowerShell window.

### Step 1: Go to frontend folder

```powershell
cd "C:\Projects\IOT\Internet of Things - IoT Vehicle Tracking & Theft Prevention System\iot_vehicle_tracking_frontend"
```

### Step 2: Install Frontend Packages

```powershell
npm install
```

### Step 3: Run Frontend

```powershell
npm run dev
```

### Step 4: Open Dashboard

```text
http://localhost:5173
```

---

## Important Windows Path Note

If the project folder contains the `&` symbol, frontend commands may fail in Windows PowerShell.

Use a clean path like this:

```text
C:\Projects\IOT\vehicle_tracking_project\
```

Recommended clean frontend command:

```powershell
cd "C:\Projects\IOT\vehicle_tracking_project\iot_vehicle_tracking_frontend"
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint          | Description                  |
| ------ | ----------------- | ---------------------------- |
| GET    | `/`               | Backend health check         |
| GET    | `/latest`         | Get latest vehicle status    |
| GET    | `/readings`       | Get all GPS/location logs    |
| POST   | `/simulate`       | Generate virtual GPS reading |
| POST   | `/manual-reading` | Add manual GPS data          |
| POST   | `/engine/lock`    | Lock engine                  |
| POST   | `/engine/unlock`  | Unlock engine                |
| GET    | `/export/csv`     | Download CSV report          |
| GET    | `/export/pdf`     | Download PDF report          |
| DELETE | `/clear`          | Clear all logs               |

---

## Sample GPS Data

```json
{
  "vehicle_id": "VH-001",
  "latitude": 18.5204,
  "longitude": 73.8567,
  "speed": 42.5,
  "geofence_status": "INSIDE",
  "distance_from_base": 125.4,
  "engine_status": "UNLOCKED",
  "alert": "NORMAL",
  "google_maps_url": "https://www.google.com/maps?q=18.5204,73.8567"
}
```

---

## Geofence Logic

The system checks whether the vehicle is inside or outside a predefined safe zone.

Example logic:

```text
If distance from base location is less than geofence radius:
    Vehicle is inside safe zone
    Alert status is NORMAL

If distance from base location is greater than geofence radius:
    Vehicle is outside safe zone
    Generate GEOFENCE ALERT

If vehicle moves while engine is locked:
    Generate THEFT ALERT
```

---

## Theft Detection Logic

Theft is detected when:

* Vehicle moves outside the geofence
* Vehicle speed is greater than allowed value while locked
* Vehicle starts moving unexpectedly
* Vehicle location changes when engine is locked

Example:

```text
If engine_status = LOCKED and speed > 5 km/h:
    Alert = THEFT DETECTED
    Buzzer = ON
    Dashboard alert = ACTIVE
```

---

## Virtual Simulation

If real GPS hardware is not available, this project supports virtual simulation.

Simulation modes include:

* Normal vehicle movement
* Vehicle parked
* Vehicle moving inside safe zone
* Vehicle leaving geofence
* Vehicle stolen
* Engine locked movement
* High-speed movement

This allows students to demonstrate the complete project without real ESP32 or GPS hardware.

---

## Dashboard Features

The dashboard displays:

* Vehicle ID
* Live latitude
* Live longitude
* Vehicle speed
* Distance from base location
* Geofence status
* Theft alert status
* Engine lock/unlock status
* Google Maps link
* Location history logs
* CSV/PDF download buttons
* Simulation controls
* Manual GPS input

---

## ESP32 Wiring

### GPS Module to ESP32

| GPS Module | ESP32   |
| ---------- | ------- |
| VCC        | 3.3V    |
| GND        | GND     |
| TX         | GPIO 16 |
| RX         | GPIO 17 |

### Relay Module to ESP32

| Relay | ESP32   |
| ----- | ------- |
| IN    | GPIO 25 |
| VCC   | 5V      |
| GND   | GND     |

### Buzzer and LED

| Component | ESP32   |
| --------- | ------- |
| Buzzer    | GPIO 26 |
| LED       | GPIO 27 |

---

## ESP32 Code Concept

```cpp
#include <TinyGPSPlus.h>

TinyGPSPlus gps;

#define RELAY_PIN 25
#define BUZZER_PIN 26

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
}

void loop() {
  float latitude = gps.location.lat();
  float longitude = gps.location.lng();
  float speed = gps.speed.kmph();

  if (speed > 5) {
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.println("Theft alert: Vehicle moving");
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }
}
```

---

## Report Generation

The system can generate a location history report containing:

* Timestamp
* Vehicle ID
* Latitude
* Longitude
* Speed
* Geofence status
* Engine status
* Alert type
* Google Maps link

Reports can be exported as:

* CSV
* PDF

---


## Applications

This project can be used in:

* Personal vehicle security
* Fleet management
* School bus monitoring
* Delivery vehicle tracking
* Logistics tracking
* Rental vehicle monitoring
* Emergency vehicle dispatch
* Transport company dashboards

---

## Industry Relevance

Vehicle tracking and theft prevention systems are used by:

* Logistics companies
* Delivery companies
* School transport services
* Cab services
* Fleet monitoring companies
* Vehicle security companies

Companies use similar systems to track vehicles, monitor routes, reduce theft risk, improve fleet efficiency, and provide better customer visibility.

---

## Learning Outcomes

By completing this project, I learned:

* How GPS-based tracking works
* How ESP32 can process GPS data
* How to create virtual GPS simulation
* How geofencing works
* How theft detection logic is implemented
* How remote engine lock/unlock simulation works
* How to build a FastAPI backend
* How to connect frontend dashboard with backend API
* How to generate CSV/PDF reports
* How to document and upload an IoT project on GitHub

---

## Future Improvements

Possible future improvements:

* Live map integration
* Mobile app alerts
* SMS alerts using GSM module
* Telegram/WhatsApp alert integration
* Accident detection using accelerometer
* Route history visualization
* Fuel monitoring
* Driver behavior analysis
* AI-based anomaly detection
* Firebase/InfluxDB cloud storage
* Real vehicle relay integration with proper safety isolation

---

## Interview Preparation

### 1. Explain your project.

This is an IoT-based Vehicle Tracking and Theft Prevention System. It tracks vehicle location using GPS coordinates and checks whether the vehicle is inside a predefined safe zone using geofencing. If unauthorized movement is detected or the vehicle leaves the safe zone, the system generates an alert. It also supports remote engine lock/unlock simulation and stores location history for reporting.

### 2. What problem does this project solve?

This project helps prevent vehicle theft and enables real-time vehicle monitoring. It allows owners or fleet managers to track vehicles remotely and receive alerts when suspicious movement is detected.

### 3. Which IoT components are used?

The project can use ESP32, NEO-6M GPS module, relay module, buzzer, LED indicators, and optionally a GSM module for SMS alerts.

### 4. How does GPS tracking work?

The GPS module receives satellite signals and provides latitude and longitude coordinates. These coordinates are processed by the ESP32 or backend and displayed on the dashboard with a Google Maps link.

### 5. What is geofencing?

Geofencing is a virtual boundary around a location. If the vehicle moves outside this boundary, the system detects it and generates an alert.

### 6. How is theft detected?

Theft is detected when the vehicle leaves the safe zone, moves while locked, or crosses a speed threshold during unauthorized movement.

### 7. How does IoT help in this project?

IoT helps send vehicle location and security data to a dashboard so the user can monitor the vehicle remotely and control engine lock/unlock status.

### 8. What outputs does the system generate?

The system generates GPS coordinates, speed, Google Maps link, geofence status, theft alerts, engine lock/unlock status, dashboard updates, and location history reports.

### 9. What challenges did you face?

Challenges included handling GPS accuracy, designing geofence logic, simulating real vehicle movement, avoiding false alerts, and connecting backend APIs with the frontend dashboard.

### 10. How can this project be improved?

It can be improved by adding live map visualization, mobile app notifications, GSM SMS alerts, accident detection, fuel monitoring, route analytics, and AI-based suspicious movement detection.

---

## GitHub Repository Details

### Repository Name

```text
IoT-Vehicle-Tracking-Theft-Prevention-System
```

### Description

```text
An IoT-based vehicle tracking and theft prevention system with GPS simulation, geofencing, theft alerts, remote engine lock/unlock, dashboard, CSV/PDF reports, and GitHub-ready documentation.
```

### GitHub Topics

```text
iot
vehicle-tracking
gps-tracking
esp32
gps
geofencing
theft-prevention
fastapi
python
react
iot-dashboard
vehicle-security
fleet-management
```

---

## Author

**Prasad Shelar**

---

## License

This project is created for educational and academic purposes. You can use and modify it for learning, college submissions, and portfolio building.

---

## Conclusion

The **IoT Vehicle Tracking & Theft Prevention System** demonstrates how IoT, GPS, geofencing, dashboards, and remote-control logic can be used to improve vehicle security. It is beginner-friendly, simulation-ready, and suitable for GitHub portfolio, academic project submission, and placement preparation.
