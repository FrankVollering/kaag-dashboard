import os
import json
import requests
from datetime import datetime, timezone

APPLICATION_KEY = os.environ[ECOWITT_APPLICATION_KEY]
API_KEY = os.environ[ECOWITT_API_KEY]
MAC = os.environ[ECOWITT_MAC]

DATA_FILE = datawind.json
MAX_POINTS = 288  # 24 hours at 5-minute intervals

def fetch_wind_speed()
    url = httpsapi.ecowitt.netapiv3devicereal_time
    params = {
        application_key APPLICATION_KEY,
        api_key API_KEY,
        mac MAC,
        call_back wind,
        wind_speed_unitid 6,  # 6 = kmh. Use 7 for mph, 9 for ms
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get(code) != 0
        raise RuntimeError(fEcowitt API error {data.get('msg')})

    wind = data[data][wind][wind_speed]
    return {
        time datetime.now(timezone.utc).isoformat(),
        value float(wind[value]),
        unit wind[unit],
    }

def load_history()
    if os.path.exists(DATA_FILE)
        with open(DATA_FILE, r) as f
            return json.load(f)
    return []

def save_history(history)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, w) as f
        json.dump(history, f, indent=2)

def main()
    history = load_history()
    point = fetch_wind_speed()
    history.append(point)
    history = history[-MAX_POINTS]  # keep only the most recent MAX_POINTS entries
    save_history(history)
    print(fSaved point {point})

if __name__ == __main__
    main()