const elements = {
  backendUrl: document.getElementById('backendUrl'),
  backendStatus: document.getElementById('backendStatus'),
  saveUrlBtn: document.getElementById('saveUrlBtn'),
  testBtn: document.getElementById('testBtn'),
  refreshBtn: document.getElementById('refreshBtn'),
  downloadCsvBtn: document.getElementById('downloadCsvBtn'),
  downloadPdfBtn: document.getElementById('downloadPdfBtn'),
  clearBtn: document.getElementById('clearBtn'),
  alertPanel: document.getElementById('alertPanel'),
  statusText: document.getElementById('statusText'),
  alertText: document.getElementById('alertText'),
  lockBadge: document.getElementById('lockBadge'),
  vehicleId: document.getElementById('vehicleId'),
  speed: document.getElementById('speed'),
  geofence: document.getElementById('geofence'),
  distance: document.getElementById('distance'),
  latitude: document.getElementById('latitude'),
  longitude: document.getElementById('longitude'),
  ignition: document.getElementById('ignition'),
  totalReadings: document.getElementById('totalReadings'),
  mapsLink: document.getElementById('mapsLink'),
  mapFrame: document.getElementById('mapFrame'),
  lastUpdated: document.getElementById('lastUpdated'),
  lockBtn: document.getElementById('lockBtn'),
  unlockBtn: document.getElementById('unlockBtn'),
  commandLog: document.getElementById('commandLog'),
  manualForm: document.getElementById('manualForm'),
  settingsForm: document.getElementById('settingsForm'),
  logsBody: document.getElementById('logsBody'),
  toast: document.getElementById('toast'),
  manualVehicleId: document.getElementById('manualVehicleId'),
  manualLat: document.getElementById('manualLat'),
  manualLon: document.getElementById('manualLon'),
  manualSpeed: document.getElementById('manualSpeed'),
  manualIgnition: document.getElementById('manualIgnition'),
  baseLat: document.getElementById('baseLat'),
  baseLon: document.getElementById('baseLon'),
  radius: document.getElementById('radius'),
  speedLimit: document.getElementById('speedLimit'),
  lockedSpeed: document.getElementById('lockedSpeed'),
};

const DEFAULT_URL = 'http://127.0.0.1:8000';
let toastTimer = null;

function getBaseUrl() {
  return elements.backendUrl.value.trim().replace(/\/+$/, '') || DEFAULT_URL;
}

function setBackendStatus(text, mode) {
  elements.backendStatus.textContent = text;
  elements.backendStatus.className = `status-pill ${mode || ''}`.trim();
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.remove('hidden');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => elements.toast.classList.add('hidden'), 3200);
}

async function apiFetch(path, options = {}) {
  const url = `${getBaseUrl()}${path}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try {
      const error = await response.json();
      message = error.detail || error.message || message;
    } catch (_) {
      // Keep default HTTP error text.
    }
    throw new Error(message);
  }

  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return response.json();
  }
  return response.text();
}

function formatNumber(value, digits = 2) {
  const number = Number(value);
  return Number.isFinite(number) ? number.toFixed(digits) : '--';
}

function boolText(value) {
  return value ? 'ON' : 'OFF';
}

function normalizeLatest(statusPayload) {
  if (statusPayload && statusPayload.latest) {
    return statusPayload.latest;
  }
  return statusPayload || {};
}

function getStatusClass(reading) {
  const alertType = String(reading.alert_type || '').toUpperCase();
  const vehicleStatus = String(reading.vehicle_status || '').toUpperCase();

  if (alertType.includes('THEFT') || vehicleStatus.includes('THEFT')) return 'danger-state';
  if (alertType.includes('GEOFENCE') || alertType.includes('OVERSPEED')) return 'warning';
  return '';
}

function badgeClass(text) {
  const value = String(text || '').toUpperCase();
  if (value.includes('THEFT') || value.includes('OUTSIDE') || value.includes('LOCKED')) return 'danger-badge';
  if (value.includes('GEOFENCE') || value.includes('OVERSPEED') || value.includes('MOVING')) return 'warn';
  if (value.includes('NORMAL') || value.includes('INSIDE') || value.includes('PARKED') || value.includes('UNLOCKED')) return 'ok';
  return '';
}

function setMap(latitude, longitude, googleMapsUrl) {
  const lat = Number(latitude);
  const lon = Number(longitude);

  if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
    elements.mapFrame.removeAttribute('src');
    elements.mapsLink.href = '#';
    return;
  }

  const zoom = 16;
  const delta = 0.008;
  const bbox = [lon - delta, lat - delta, lon + delta, lat + delta].join('%2C');
  elements.mapFrame.src = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat}%2C${lon}`;
  elements.mapsLink.href = googleMapsUrl || `https://www.google.com/maps?q=${lat},${lon}`;
}

function updateLatestUI(reading, totalReadings = null) {
  const latest = normalizeLatest(reading);

  elements.statusText.textContent = latest.vehicle_status || 'NO DATA';
  elements.alertText.textContent = latest.alert_message || latest.message || 'No alert message';
  elements.alertPanel.className = `panel alert-panel ${getStatusClass(latest)}`.trim();

  const locked = Boolean(latest.engine_locked);
  elements.lockBadge.textContent = locked ? 'LOCKED' : 'UNLOCKED';
  elements.lockBadge.className = `lock-badge ${locked ? 'locked' : 'unlocked'}`;

  elements.vehicleId.textContent = latest.vehicle_id || '--';
  elements.speed.textContent = formatNumber(latest.speed_kmph, 1);
  elements.geofence.textContent = latest.geofence_status || '--';
  elements.distance.textContent = formatNumber(latest.distance_from_base_m, 1);
  elements.latitude.textContent = latest.latitude !== undefined ? formatNumber(latest.latitude, 6) : '--';
  elements.longitude.textContent = latest.longitude !== undefined ? formatNumber(latest.longitude, 6) : '--';
  elements.ignition.textContent = latest.ignition_on === undefined ? '--' : boolText(latest.ignition_on);
  elements.lastUpdated.textContent = `Last updated: ${latest.timestamp || '--'} | Source: ${latest.source || '--'}`;

  if (totalReadings !== null && totalReadings !== undefined) {
    elements.totalReadings.textContent = totalReadings;
  }

  if (latest.vehicle_id) {
    elements.manualVehicleId.value = latest.vehicle_id;
  }
  if (latest.latitude !== undefined) {
    elements.manualLat.value = Number(latest.latitude).toFixed(6);
  }
  if (latest.longitude !== undefined) {
    elements.manualLon.value = Number(latest.longitude).toFixed(6);
  }

  setMap(latest.latitude, latest.longitude, latest.google_maps_url);
}

function renderLogs(logs) {
  if (!Array.isArray(logs) || logs.length === 0) {
    elements.logsBody.innerHTML = '<tr><td colspan="8" class="empty">No logs yet</td></tr>';
    return;
  }

  const reversed = [...logs].reverse();
  elements.logsBody.innerHTML = reversed.map((row) => {
    const location = `${formatNumber(row.latitude, 5)}, ${formatNumber(row.longitude, 5)}`;
    const mapsHref = row.google_maps_url || `https://www.google.com/maps?q=${row.latitude},${row.longitude}`;
    return `
      <tr>
        <td>${row.timestamp || '--'}</td>
        <td>${row.vehicle_id || '--'}</td>
        <td><a class="badge" href="${mapsHref}" target="_blank" rel="noopener">${location}</a></td>
        <td>${formatNumber(row.speed_kmph, 1)} km/h</td>
        <td><span class="badge ${badgeClass(row.engine_locked ? 'LOCKED' : 'UNLOCKED')}">${row.engine_locked ? 'LOCKED' : 'UNLOCKED'}</span></td>
        <td><span class="badge ${badgeClass(row.geofence_status)}">${row.geofence_status || '--'}</span></td>
        <td><span class="badge ${badgeClass(row.vehicle_status)}">${row.vehicle_status || '--'}</span></td>
        <td>${row.alert_message || row.alert_type || '--'}</td>
      </tr>
    `;
  }).join('');
}

function fillSettings(settings) {
  if (!settings) return;
  elements.baseLat.value = settings.base_latitude ?? '';
  elements.baseLon.value = settings.base_longitude ?? '';
  elements.radius.value = settings.geofence_radius_m ?? '';
  elements.speedLimit.value = settings.speed_limit_kmph ?? '';
  elements.lockedSpeed.value = settings.locked_speed_threshold_kmph ?? '';
}

async function testBackend() {
  try {
    const health = await apiFetch('/api/health');
    setBackendStatus('Backend connected', 'connected');
    showToast(health.message || 'Backend connected');
    return true;
  } catch (error) {
    setBackendStatus('Connection error', 'error');
    showToast(`Backend connection error: ${error.message}`);
    return false;
  }
}

async function refreshDashboard() {
  try {
    const status = await apiFetch('/api/status');
    setBackendStatus('Backend connected', 'connected');
    fillSettings(status.settings);
    updateLatestUI(status.latest || {}, status.total_readings || 0);

    const logPayload = await apiFetch('/api/logs?limit=50');
    renderLogs(logPayload.logs || []);
  } catch (error) {
    setBackendStatus('Connection error', 'error');
    showToast(`Backend connection error: ${error.message}`);
  }
}

async function simulate(mode) {
  try {
    const payload = await apiFetch('/api/simulate', {
      method: 'POST',
      body: JSON.stringify({ mode }),
    });
    updateLatestUI(payload.reading);
    showToast(`Simulation saved: ${mode}`);
    await refreshDashboard();
  } catch (error) {
    showToast(`Simulation error: ${error.message}`);
  }
}

async function sendCommand(command) {
  try {
    const payload = await apiFetch('/api/command', {
      method: 'POST',
      body: JSON.stringify({ command }),
    });
    elements.commandLog.textContent = `${payload.message} at ${new Date().toLocaleTimeString()}`;
    showToast(payload.message || `Command sent: ${command}`);
    await refreshDashboard();
  } catch (error) {
    showToast(`Command error: ${error.message}`);
  }
}

async function saveManualReading(event) {
  event.preventDefault();
  const payload = {
    vehicle_id: elements.manualVehicleId.value.trim() || 'VEH-001',
    latitude: Number(elements.manualLat.value),
    longitude: Number(elements.manualLon.value),
    speed_kmph: Number(elements.manualSpeed.value),
    ignition_on: elements.manualIgnition.checked,
    source: 'manual',
  };

  if (!Number.isFinite(payload.latitude) || !Number.isFinite(payload.longitude) || !Number.isFinite(payload.speed_kmph)) {
    showToast('Please enter valid latitude, longitude and speed.');
    return;
  }

  try {
    const result = await apiFetch('/api/manual', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    updateLatestUI(result.reading);
    showToast('Manual reading saved');
    await refreshDashboard();
  } catch (error) {
    showToast(`Manual reading error: ${error.message}`);
  }
}

async function saveSettings(event) {
  event.preventDefault();
  const payload = {
    base_latitude: Number(elements.baseLat.value),
    base_longitude: Number(elements.baseLon.value),
    geofence_radius_m: Number(elements.radius.value),
    speed_limit_kmph: Number(elements.speedLimit.value),
    locked_speed_threshold_kmph: Number(elements.lockedSpeed.value),
  };

  const invalid = Object.values(payload).some((value) => !Number.isFinite(value));
  if (invalid) {
    showToast('Please enter valid setting values.');
    return;
  }

  try {
    const result = await apiFetch('/api/settings', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    fillSettings(result.settings);
    showToast('Settings saved');
    await refreshDashboard();
  } catch (error) {
    showToast(`Settings error: ${error.message}`);
  }
}

async function clearLogs() {
  const ok = confirm('Clear all backend CSV logs?');
  if (!ok) return;

  try {
    await apiFetch('/api/clear', { method: 'POST' });
    showToast('Logs cleared');
    await refreshDashboard();
  } catch (error) {
    showToast(`Clear logs error: ${error.message}`);
  }
}

function openDownload(path) {
  window.open(`${getBaseUrl()}${path}`, '_blank', 'noopener');
}

function saveBackendUrl() {
  const url = getBaseUrl();
  elements.backendUrl.value = url;
  localStorage.setItem('vehicleBackendUrl', url);
  showToast('Backend URL saved');
}

function init() {
  const savedUrl = localStorage.getItem('vehicleBackendUrl');
  if (savedUrl) elements.backendUrl.value = savedUrl;

  elements.saveUrlBtn.addEventListener('click', saveBackendUrl);
  elements.testBtn.addEventListener('click', testBackend);
  elements.refreshBtn.addEventListener('click', refreshDashboard);
  elements.downloadCsvBtn.addEventListener('click', () => openDownload('/api/download/csv'));
  elements.downloadPdfBtn.addEventListener('click', () => openDownload('/api/download/pdf'));
  elements.clearBtn.addEventListener('click', clearLogs);
  elements.lockBtn.addEventListener('click', () => sendCommand('LOCK'));
  elements.unlockBtn.addEventListener('click', () => sendCommand('UNLOCK'));
  elements.manualForm.addEventListener('submit', saveManualReading);
  elements.settingsForm.addEventListener('submit', saveSettings);

  document.querySelectorAll('[data-mode]').forEach((button) => {
    button.addEventListener('click', () => simulate(button.dataset.mode));
  });

  refreshDashboard();
  setInterval(refreshDashboard, 5000);
}

init();
