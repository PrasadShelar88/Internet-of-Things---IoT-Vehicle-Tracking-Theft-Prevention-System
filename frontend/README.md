# IoT Vehicle Tracking & Theft Prevention Frontend

This is the frontend dashboard for the FastAPI backend project.

## Run Backend First

Open PowerShell in the backend folder and run:

```powershell
.\run_backend.bat
```

Backend URL:

```text
http://127.0.0.1:8000
```

## Run Frontend

Open PowerShell in this frontend folder and run:

```powershell
.\run_frontend.bat
```

Then open:

```text
http://127.0.0.1:5500
```

## Features

- Backend connection testing
- Live GPS dashboard
- Vehicle status and theft alert banner
- Engine lock/unlock commands
- Virtual GPS simulation
- Manual GPS reading form
- Geofence and speed threshold settings
- Recent route history table
- Google Maps link
- CSV and PDF report downloads
- Clear logs button

## Matching Backend API

This frontend uses these routes:

- `GET /api/health`
- `GET /api/status`
- `GET /api/logs?limit=50`
- `POST /api/simulate`
- `POST /api/manual`
- `POST /api/command`
- `POST /api/settings`
- `POST /api/clear`
- `GET /api/download/csv`
- `GET /api/download/pdf`
