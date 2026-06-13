from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime
import csv
import json
import math
import random

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

APP_TITLE = "IoT Vehicle Tracking & Theft Prevention Backend"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOG_FILE = DATA_DIR / "vehicle_logs.csv"
SETTINGS_FILE = DATA_DIR / "settings.json"
STATE_FILE = DATA_DIR / "state.json"

DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

CSV_FIELDS = [
    "timestamp",
    "vehicle_id",
    "latitude",
    "longitude",
    "speed_kmph",
    "ignition_on",
    "engine_locked",
    "distance_from_base_m",
    "geofence_status",
    "vehicle_status",
    "alert_type",
    "alert_message",
    "google_maps_url",
    "source",
]

DEFAULT_SETTINGS = {
    "vehicle_id": "VEH-001",
    "base_latitude": 18.6298,
    "base_longitude": 73.7997,
    "geofence_radius_m": 200.0,
    "speed_limit_kmph": 80.0,
    "locked_speed_threshold_kmph": 5.0,
}

DEFAULT_STATE = {
    "engine_locked": False,
    "last_command": "UNLOCK",
    "last_command_time": None,
}


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_log_file() -> None:
    if not LOG_FILE.exists():
        with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def read_json_file(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        path.write_text(json.dumps(default, indent=2), encoding="utf-8")
        return default.copy()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        merged = default.copy()
        merged.update(data)
        return merged
    except Exception:
        path.write_text(json.dumps(default, indent=2), encoding="utf-8")
        return default.copy()


def write_json_file(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_settings() -> Dict[str, Any]:
    return read_json_file(SETTINGS_FILE, DEFAULT_SETTINGS)


def save_settings(data: Dict[str, Any]) -> Dict[str, Any]:
    current = get_settings()
    current.update({k: v for k, v in data.items() if v is not None})
    write_json_file(SETTINGS_FILE, current)
    return current


def get_state() -> Dict[str, Any]:
    return read_json_file(STATE_FILE, DEFAULT_STATE)


def save_state(data: Dict[str, Any]) -> Dict[str, Any]:
    current = get_state()
    current.update(data)
    write_json_file(STATE_FILE, current)
    return current


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_m = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_m * c


def coordinate_offset(lat: float, lon: float, north_m: float, east_m: float) -> tuple[float, float]:
    # Good approximation for small simulation offsets.
    new_lat = lat + north_m / 111_320
    new_lon = lon + east_m / (111_320 * math.cos(math.radians(lat)))
    return round(new_lat, 6), round(new_lon, 6)


def maps_url(lat: float, lon: float) -> str:
    return f"https://www.google.com/maps?q={lat:.6f},{lon:.6f}"


def read_logs(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    ensure_log_file()
    with LOG_FILE.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows = rows[-limit:] if limit and limit > 0 else rows
    return [normalize_row(row) for row in rows]


def normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    numeric_fields = ["latitude", "longitude", "speed_kmph", "distance_from_base_m"]
    for field in numeric_fields:
        try:
            row[field] = float(row[field])
        except Exception:
            pass
    for field in ["ignition_on", "engine_locked"]:
        value = row.get(field)
        if isinstance(value, str):
            row[field] = value.lower() in ["true", "1", "yes", "on"]
    return row


def append_log(row: Dict[str, Any]) -> None:
    ensure_log_file()
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow({field: row.get(field, "") for field in CSV_FIELDS})


def analyse_reading(
    vehicle_id: str,
    latitude: float,
    longitude: float,
    speed_kmph: float,
    ignition_on: bool,
    source: str,
) -> Dict[str, Any]:
    settings = get_settings()
    state = get_state()
    engine_locked = bool(state.get("engine_locked", False))

    distance_m = haversine_m(
        float(settings["base_latitude"]),
        float(settings["base_longitude"]),
        latitude,
        longitude,
    )
    outside_geofence = distance_m > float(settings["geofence_radius_m"])
    over_speed = speed_kmph > float(settings["speed_limit_kmph"])
    locked_movement = engine_locked and speed_kmph > float(settings["locked_speed_threshold_kmph"])
    locked_ignition = engine_locked and ignition_on

    alert_parts = []
    if outside_geofence:
        alert_parts.append(f"Vehicle outside safe zone: {distance_m:.1f} m from base")
    if locked_movement:
        alert_parts.append("Movement detected while engine is locked")
    if locked_ignition:
        alert_parts.append("Ignition is ON while engine lock is active")
    if over_speed:
        alert_parts.append(f"Speed {speed_kmph:.1f} km/h exceeds limit {float(settings['speed_limit_kmph']):.1f} km/h")

    if locked_movement or locked_ignition:
        alert_type = "THEFT_ALERT"
        vehicle_status = "THEFT_ALERT"
    elif outside_geofence:
        alert_type = "GEOFENCE_ALERT"
        vehicle_status = "GEOFENCE_ALERT"
    elif over_speed:
        alert_type = "OVERSPEED_ALERT"
        vehicle_status = "OVERSPEED_ALERT"
    elif speed_kmph <= 1:
        alert_type = "NORMAL"
        vehicle_status = "PARKED"
    else:
        alert_type = "NORMAL"
        vehicle_status = "MOVING"

    row = {
        "timestamp": now_iso(),
        "vehicle_id": vehicle_id or settings["vehicle_id"],
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "speed_kmph": round(speed_kmph, 2),
        "ignition_on": bool(ignition_on),
        "engine_locked": engine_locked,
        "distance_from_base_m": round(distance_m, 2),
        "geofence_status": "OUTSIDE" if outside_geofence else "INSIDE",
        "vehicle_status": vehicle_status,
        "alert_type": alert_type,
        "alert_message": "; ".join(alert_parts) if alert_parts else "NORMAL",
        "google_maps_url": maps_url(latitude, longitude),
        "source": source,
    }
    append_log(row)
    return row


class ManualReading(BaseModel):
    vehicle_id: Optional[str] = Field(default=None, examples=["VEH-001"])
    latitude: float = Field(..., ge=-90, le=90, examples=[18.6298])
    longitude: float = Field(..., ge=-180, le=180, examples=[73.7997])
    speed_kmph: float = Field(default=0, ge=0, examples=[35])
    ignition_on: bool = Field(default=True)
    source: Optional[str] = Field(default="manual")


class CommandBody(BaseModel):
    command: str = Field(..., examples=["LOCK"])


class SettingsUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    base_latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    base_longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    geofence_radius_m: Optional[float] = Field(default=None, gt=0)
    speed_limit_kmph: Optional[float] = Field(default=None, gt=0)
    locked_speed_threshold_kmph: Optional[float] = Field(default=None, ge=0)


class SimulateBody(BaseModel):
    mode: Optional[str] = Field(default="normal", examples=["normal"])
    vehicle_id: Optional[str] = None


ensure_log_file()
get_settings()
get_state()

app = FastAPI(title=APP_TITLE, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "message": "Backend connected",
        "project": "IoT Vehicle Tracking & Theft Prevention System",
        "docs": "http://127.0.0.1:8000/docs",
        "health": "http://127.0.0.1:8000/health",
        "latest": "http://127.0.0.1:8000/api/latest",
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "message": "Backend connected", "time": now_iso()}


@app.get("/api/health")
def api_health() -> Dict[str, Any]:
    return health()


@app.get("/api/status")
def api_status() -> Dict[str, Any]:
    logs = read_logs(limit=1)
    latest = logs[-1] if logs else None
    return {
        "backend": "connected",
        "project": "IoT Vehicle Tracking & Theft Prevention System",
        "settings": get_settings(),
        "state": get_state(),
        "latest": latest,
        "total_readings": len(read_logs()),
    }


@app.get("/api/latest")
def latest() -> Dict[str, Any]:
    logs = read_logs(limit=1)
    if not logs:
        settings = get_settings()
        return {
            "message": "No readings yet. Use /api/simulate or /api/manual to add data.",
            "vehicle_id": settings["vehicle_id"],
            "latitude": settings["base_latitude"],
            "longitude": settings["base_longitude"],
            "speed_kmph": 0,
            "engine_locked": get_state().get("engine_locked", False),
            "vehicle_status": "NO_DATA",
            "alert_type": "NORMAL",
            "alert_message": "No readings yet",
            "google_maps_url": maps_url(float(settings["base_latitude"]), float(settings["base_longitude"])),
        }
    return logs[-1]


@app.get("/api/logs")
def logs(limit: int = Query(default=100, ge=1, le=5000)) -> Dict[str, Any]:
    rows = read_logs(limit=limit)
    return {"count": len(rows), "logs": rows}


@app.get("/api/readings")
def readings(limit: int = Query(default=100, ge=1, le=5000)) -> Dict[str, Any]:
    return logs(limit=limit)


@app.post("/api/manual")
def manual_reading(reading: ManualReading) -> Dict[str, Any]:
    settings = get_settings()
    row = analyse_reading(
        vehicle_id=reading.vehicle_id or settings["vehicle_id"],
        latitude=reading.latitude,
        longitude=reading.longitude,
        speed_kmph=reading.speed_kmph,
        ignition_on=reading.ignition_on,
        source=reading.source or "manual",
    )
    return {"saved": True, "reading": row}


@app.post("/api/readings")
def save_reading(reading: ManualReading) -> Dict[str, Any]:
    return manual_reading(reading)


def make_simulated_reading(mode: str, vehicle_id: Optional[str] = None) -> Dict[str, Any]:
    settings = get_settings()
    mode = (mode or "normal").strip().lower()
    base_lat = float(settings["base_latitude"])
    base_lon = float(settings["base_longitude"])
    vehicle = vehicle_id or settings["vehicle_id"]

    if mode in ["parked", "stop", "idle"]:
        lat, lon = coordinate_offset(base_lat, base_lon, random.uniform(-4, 4), random.uniform(-4, 4))
        speed = random.uniform(0, 0.8)
        ignition = False
    elif mode in ["theft", "locked_move", "stolen"]:
        save_state({"engine_locked": True, "last_command": "LOCK", "last_command_time": now_iso()})
        lat, lon = coordinate_offset(base_lat, base_lon, random.uniform(280, 650), random.uniform(280, 650))
        speed = random.uniform(25, 55)
        ignition = True
    elif mode in ["outside", "outside_geofence", "geofence"]:
        lat, lon = coordinate_offset(base_lat, base_lon, random.uniform(250, 550), random.uniform(-500, 500))
        speed = random.uniform(15, 45)
        ignition = True
    elif mode in ["overspeed", "speeding"]:
        lat, lon = coordinate_offset(base_lat, base_lon, random.uniform(-50, 50), random.uniform(-50, 50))
        speed = random.uniform(float(settings["speed_limit_kmph"]) + 5, float(settings["speed_limit_kmph"]) + 35)
        ignition = True
    elif mode in ["unlock_normal", "normal_unlocked"]:
        save_state({"engine_locked": False, "last_command": "UNLOCK", "last_command_time": now_iso()})
        lat, lon = coordinate_offset(base_lat, base_lon, random.uniform(-80, 80), random.uniform(-80, 80))
        speed = random.uniform(10, 45)
        ignition = True
    else:
        lat, lon = coordinate_offset(base_lat, base_lon, random.uniform(-90, 90), random.uniform(-90, 90))
        speed = random.uniform(8, 45)
        ignition = True

    return analyse_reading(vehicle, lat, lon, speed, ignition, f"simulation:{mode}")


@app.post("/api/simulate")
def simulate_post(body: Optional[SimulateBody] = None, mode: Optional[str] = Query(default=None)) -> Dict[str, Any]:
    selected_mode = mode or (body.mode if body else "normal")
    vehicle_id = body.vehicle_id if body else None
    row = make_simulated_reading(selected_mode, vehicle_id)
    return {"saved": True, "mode": selected_mode, "reading": row}


@app.get("/api/simulate")
def simulate_get(mode: str = Query(default="normal")) -> Dict[str, Any]:
    row = make_simulated_reading(mode, None)
    return {"saved": True, "mode": mode, "reading": row}


@app.post("/api/command")
def command(body: CommandBody) -> Dict[str, Any]:
    command_value = body.command.strip().upper()
    if command_value not in ["LOCK", "UNLOCK"]:
        raise HTTPException(status_code=400, detail="Command must be LOCK or UNLOCK")
    new_state = save_state({
        "engine_locked": command_value == "LOCK",
        "last_command": command_value,
        "last_command_time": now_iso(),
    })
    return {
        "success": True,
        "command": command_value,
        "engine_locked": new_state["engine_locked"],
        "message": "Engine locked" if command_value == "LOCK" else "Engine unlocked",
    }


@app.post("/api/lock")
def lock_engine() -> Dict[str, Any]:
    return command(CommandBody(command="LOCK"))


@app.post("/api/unlock")
def unlock_engine() -> Dict[str, Any]:
    return command(CommandBody(command="UNLOCK"))


@app.get("/api/settings")
def settings() -> Dict[str, Any]:
    return get_settings()


@app.post("/api/settings")
def update_settings(update: SettingsUpdate) -> Dict[str, Any]:
    return {"saved": True, "settings": save_settings(update.model_dump(exclude_unset=True))}


@app.post("/api/clear")
def clear_logs() -> Dict[str, Any]:
    ensure_log_file()
    with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
    return {"success": True, "message": "Logs cleared"}


@app.delete("/api/clear")
def clear_logs_delete() -> Dict[str, Any]:
    return clear_logs()


@app.post("/api/clear_logs")
def clear_logs_alias() -> Dict[str, Any]:
    return clear_logs()


@app.get("/api/download/csv")
def download_csv() -> FileResponse:
    ensure_log_file()
    return FileResponse(str(LOG_FILE), media_type="text/csv", filename="vehicle_location_history.csv")


def build_text_pdf_fallback(rows: List[Dict[str, Any]], path: Path) -> None:
    # Minimal fallback: writes a readable text report with .pdf extension if reportlab is unavailable.
    # Install requirements.txt to get a real PDF report.
    lines = ["IoT Vehicle Tracking & Theft Prevention Report", "=" * 55, ""]
    for row in rows:
        lines.append(
            f"{row.get('timestamp')} | {row.get('vehicle_id')} | "
            f"{row.get('latitude')}, {row.get('longitude')} | "
            f"{row.get('speed_kmph')} km/h | {row.get('vehicle_status')} | {row.get('alert_message')}"
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def generate_pdf_report() -> Path:
    rows = read_logs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = REPORTS_DIR / f"vehicle_location_report_{timestamp}.pdf"

    if not REPORTLAB_AVAILABLE:
        build_text_pdf_fallback(rows, pdf_path)
        return pdf_path

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=24, leftMargin=24, topMargin=24, bottomMargin=24)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("IoT Vehicle Tracking & Theft Prevention Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Generated: {now_iso()}", styles["Normal"]),
        Paragraph(f"Total readings: {len(rows)}", styles["Normal"]),
        Spacer(1, 12),
    ]

    table_data = [["Time", "Vehicle", "Lat", "Lon", "Speed", "Status", "Alert"]]
    for row in rows[-40:]:
        table_data.append([
            str(row.get("timestamp", "")),
            str(row.get("vehicle_id", "")),
            f"{float(row.get('latitude', 0)):.5f}" if row.get("latitude") != "" else "",
            f"{float(row.get('longitude', 0)):.5f}" if row.get("longitude") != "" else "",
            str(row.get("speed_kmph", "")),
            str(row.get("vehicle_status", "")),
            str(row.get("alert_type", "")),
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Note: PDF shows latest 40 readings. Full history is available in CSV.", styles["Italic"]))
    doc.build(story)
    return pdf_path


@app.get("/api/download/pdf")
def download_pdf() -> FileResponse:
    pdf_path = generate_pdf_report()
    return FileResponse(str(pdf_path), media_type="application/pdf", filename=pdf_path.name)


# Extra aliases for beginner frontends that may call simpler paths.
@app.get("/latest")
def latest_alias() -> Dict[str, Any]:
    return latest()


@app.get("/logs")
def logs_alias(limit: int = Query(default=100, ge=1, le=5000)) -> Dict[str, Any]:
    return logs(limit=limit)


@app.post("/simulate")
def simulate_alias(body: Optional[SimulateBody] = None, mode: Optional[str] = Query(default=None)) -> Dict[str, Any]:
    return simulate_post(body=body, mode=mode)


@app.post("/manual")
def manual_alias(reading: ManualReading) -> Dict[str, Any]:
    return manual_reading(reading)


@app.post("/command")
def command_alias(body: CommandBody) -> Dict[str, Any]:
    return command(body)
