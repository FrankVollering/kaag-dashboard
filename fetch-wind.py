import os
import json
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

STATION_TZ = ZoneInfo("Europe/Amsterdam")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

APPLICATION_KEY = os.environ["ECOWITT_APPLICATION_KEY"]
API_KEY = os.environ["ECOWITT_API_KEY"]
MAC = os.environ["ECOWITT_MAC"]

DATA_FILE = "data/wind.json"

def fetch_wind_history():
    # the API interprets start/end date strings in the station's local time,
    # so build them in that timezone (not UTC) to get the full day up to now
    now = datetime.now(STATION_TZ)
    start_date = now.strftime("%Y-%m-%d 00:00:00")
    end_date = now.strftime("%Y-%m-%d %H:%M:%S")

    url = "https://api.ecowitt.net/api/v3/device/history"
    params = {
        "application_key": APPLICATION_KEY,
        "api_key": API_KEY,
        "mac": MAC,
        "call_back": "wind",
        "start_date": start_date,
        "end_date": end_date,
        "cycle_type": "5min",
        "wind_speed_unitid": 6,  # API currently returns m/s regardless
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != 0:
        raise RuntimeError(f"Ecowitt API error: {data.get('msg')}")

    wind = data["data"]["wind"]
    speeds = wind["wind_speed"]["list"]
    gusts = wind["wind_gust"]["list"]
    directions = wind["wind_direction"]["list"]

    points = []
    for ts in sorted(speeds, key=int):
        points.append({
            "time": datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat(),
            "speed": float(speeds[ts]),
            "gust": float(gusts[ts]) if ts in gusts else None,
            "direction": int(directions[ts]) if ts in directions else None,
        })
    return {
        "unit": wind["wind_speed"]["unit"],
        "points": points,
    }

def save_history(history):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=2)

def main():
    history = fetch_wind_history()
    save_history(history)
    print(f"Saved {len(history['points'])} points ({history['unit']})")

if __name__ == "__main__":
    main()
