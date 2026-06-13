#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Starting Vehicle Tracking frontend at http://127.0.0.1:5500"
python3 -m http.server 5500
