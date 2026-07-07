import os
import json
import time
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
MAX_RETRIES = 4
INITIAL_BACKOFF = 2  # seconds, doubles each retry

def _get_with_retries(url, params):
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", INITIAL_BACKOFF * 2 ** (attempt - 1)))
                print(f"Rate limited (429), attempt {attempt}/{MAX_RETRIES}, waiting {wait}s")
                last_error = RuntimeError("Ecowitt API rate limited (429)")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            last_error = e
            if attempt < MAX_RETRIES:
                wait = INITIAL_BACKOFF * 2 ** (attempt - 1)
                print(f"Request failed ({e}), attempt {attempt}/{MAX_RETRIES}, retrying in {wait}s")
                time.sleep(wait)

    raise RuntimeError(f"Ecowitt API request failed after {MAX_RETRIES} attempts: {last_error}") from last_error

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
    data = _get_with_retries(url, params)

    if data.get("code") != 0:
        raise RuntimeError(f"Ecowitt API error: {data.get('msg')}")

    try:
        wind = data["data"]["wind"]
        speeds = wind["wind_speed"]["list"]
        gusts = wind["wind_gust"]["list"]
        directions = wind["wind_direction"]["list"]
    except (KeyError, TypeError) as e:
        raise RuntimeError(f"Unexpected Ecowitt response shape: missing {e}") from e

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
