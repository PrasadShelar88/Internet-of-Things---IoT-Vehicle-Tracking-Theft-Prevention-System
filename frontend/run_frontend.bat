@echo off
setlocal
cd /d "%~dp0"

echo Starting Vehicle Tracking frontend at http://127.0.0.1:5500
echo Keep this window open while using the dashboard.
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    py -m http.server 5500
    goto :eof
)

where python >nul 2>nul
if %errorlevel%==0 (
    python -m http.server 5500
    goto :eof
)

echo Python was not found. Please install Python or open index.html directly.
pause
