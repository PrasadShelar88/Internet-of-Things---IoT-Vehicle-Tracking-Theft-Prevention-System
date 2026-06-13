# IoT Vehicle Tracking & Theft Prevention Backend

This is a ready-to-run FastAPI backend for the **IoT Vehicle Tracking & Theft Prevention System**.
It supports real GPS/manual readings, virtual simulation, geofence checking, theft detection, engine lock/unlock commands, CSV logging, and PDF report download.

## 1. How to Run on Windows

1. Extract the ZIP.
2. Open the extracted `vehicle_tracking_backend` folder.
3. Double-click:

```bat
run_backend.bat
```

Or run manually in PowerShell:

```powershell
cd "C:\Projects\IOT\vehicle_tracking_backend"
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 2. Main API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Test backend connection |
| GET | `/health` | Backend health check |
| GET | `/api/status` | Settings, state, latest reading, total readings |
| GET | `/api/latest` | Latest vehicle GPS/status reading |
| GET | `/api/logs` | Location history logs |
| POST | `/api/manual` | Save manual GPS reading |
| POST/GET | `/api/simulate?mode=normal` | Generate virtual GPS reading |
| POST | `/api/command` | Send `LOCK` or `UNLOCK` command |
| POST | `/api/lock` | Lock engine/relay |
| POST | `/api/unlock` | Unlock engine/relay |
| GET | `/api/download/csv` | Download CSV report |
| GET | `/api/download/pdf` | Download PDF report |
| POST | `/api/clear` | Clear all logs |

## 3. Simulation Modes

Use these modes from your frontend or browser/API docs:

```text
normal
parked
theft
locked_move
outside_geofence
overspeed
unlock_normal
```

Examples:

```text
http://127.0.0.1:8000/api/simulate?mode=normal
http://127.0.0.1:8000/api/simulate?mode=theft
http://127.0.0.1:8000/api/simulate?mode=outside_geofence
```

## 4. Manual Reading Example

POST to `/api/manual`:

```json
{
  "vehicle_id": "VEH-001",
  "latitude": 18.6298,
  "longitude": 73.7997,
  "speed_kmph": 35,
  "ignition_on": true,
  "source": "manual"
}
```

## 5. Lock / Unlock Example

POST to `/api/command`:

```json
{
  "command": "LOCK"
}
```

or:

```json
{
  "command": "UNLOCK"
}
```

## 6. Geofence and Theft Logic

Default safe zone:

```text
Base Latitude: 18.6298
Base Longitude: 73.7997
Radius: 200 meters
```

Alerts are generated when:

- Vehicle leaves geofence.
- Vehicle moves while engine is locked.
- Ignition is ON while lock is active.
- Vehicle speed crosses speed limit.

## 7. Data Storage

Logs are stored here:

```text
data/vehicle_logs.csv
```

Settings are stored here:

```text
data/settings.json
```

Engine lock state is stored here:

```text
data/state.json
```

## 8. Recommended Frontend Backend URL

Use this in your frontend:

```text
http://127.0.0.1:8000
```

If your frontend gets `Not Found`, make sure it uses endpoints like:

```text
/api/latest
/api/logs
/api/simulate
/api/manual
/api/command
/api/download/csv
/api/download/pdf
```

## 9. GitHub Ready

Suggested repository name:

```text
IoT-Vehicle-Tracking-Theft-Prevention-System
```

Suggested commit plan:

```text
git init
git add .
git commit -m "Add FastAPI backend for vehicle tracking system"
```
