# Import packages
import requests
import pandas as pd
from datetime import datetime, timezone

# OpenSky API query function
print("Hello World")

def fetch_arrivals(airport_icao, minutes_back):
    # Questy arrivals in the last hour
    now = datetime.utcnow()
    end = int(now.timestamp())
    begin = end - minutes_back*60

    print(end)
    print(begin)

    url = f"https://opensky-network.org/api/flights/arrival"
    params = {
        "airport": airport_icao,
        "begin": begin,
        "end": end
    }

    print(f"Querying arrivals between {begin} and {end}...")

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return pd.DataFrame()
    
def clean_arrivals(arrivals):
    if arrivals.empty:
        print("No arrival data found.")
        return arrivals

    arrivals = arrivals.copy()
    arrivals['callsign'] = arrivals['callsign'].str.strip()
    arrivals['arrival_time'] = pd.to_datetime(arrivals['lastSeen'], unit='s')
    arrivals['origin'] = arrivals['estDepartureAirport']
    arrivals['icao24'] = arrivals['icao24'].str.upper()

    return arrivals[['arrival_time', 'callsign', 'origin', 'icao24']]

if __name__ == "__main__":
    arrivals = fetch_arrivals(airport_icao="LSZH", minutes_back=30)
    clean_arrivals = clean_arrivals(arrivals)
    print(clean_arrivals)
    clean_arrivals.to_csv("arrivals.csv")