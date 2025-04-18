# Import packages
import requests
import pandas as pd
from datetime import datetime, timezone

# At the moment, this function returns "descending" aircraft only
def fetch_aircraft_nearby():
    # Bounding box around LSZH
    params = {
    'lamin': 47.1947,
    'lamax': 47.7347,
    'lomin': 8.1392,
    'lomax': 8.9592
    }
    response = requests.get(
    "https://opensky-network.org/api/states/all",
    params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Aircraft found: {len(data['states'])}")
        # New data frame for aircraft in final approach
        final_approach_aircraft = pd.DataFrame(columns=["Callsign", "Altitude", "Descent Rate"])
        for state in data['states']:
            callsign = state[1].strip() if state[1] else "N/A"
            altitude = state[7]
            vertical_rate = state[11]
            if altitude is not None and vertical_rate is not None and int(altitude) < 3000 and int(vertical_rate) < 0:
                new_aircraft = {"Callsign": [callsign], "Altitude": [altitude], "Descent Rate": [vertical_rate]}
                final_approach_aircraft = pd.concat([final_approach_aircraft, pd.DataFrame(new_aircraft)], ignore_index=True)
        final_approach_aircraft = final_approach_aircraft.sort_values(by="Altitude")
        return(final_approach_aircraft)  
    else:
        print(f"Error {response.status_code}: {response.text}")
        return(False)

if __name__ == "__main__":
    #arrivals = fetch_arrivals(airport_icao="LSZH", minutes_back=30)
    #clean_arrivals = clean_arrivals(arrivals)
    test = fetch_aircraft_nearby()
    test.to_csv("arrivals.csv")
    print(test)