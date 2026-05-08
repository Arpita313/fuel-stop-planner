import os
import pandas as pd
import requests

def get_route(start_coords, finish_coords):
    # API Key verify karein
    api_key = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjAxNTQ5YWQ1ZDE5MDQyYjZiNTkxN2Q4YjMwMDNjMDA1IiwiaCI6Im11cm11cjY0In0='
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_coords}&end={finish_coords}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, 0
            
        data = response.json()
        geometry = data['features'][0]['geometry']['coordinates']
        dist_meters = data['features'][0]['properties']['summary']['distance']
        return geometry, (dist_meters / 1609.34) # Miles conversion
    except Exception:
        return None, 0

def calculate_fuel_plan(total_miles, geometry):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # CSV ka naam check karein: fuel-prices-optimized.csv ya fuel-prices.csv
    csv_path = os.path.join(base_dir, 'data', 'fuel-prices-optimized.csv')
    
    try:
        if not os.path.exists(csv_path):
            # Backup check agar file name different ho
            csv_path = os.path.join(base_dir, 'data', 'fuel-prices.csv')
            
        df = pd.read_csv(csv_path)
        df['Retail Price'] = pd.to_numeric(df['Retail Price'], errors='coerce')
        df = df.dropna(subset=['Retail Price', 'Truckstop Name'])
    except Exception as e:
        raise Exception(f"CSV Error: {str(e)}")

    fuel_stops = []
    total_cost = 0
    miles_covered = 0
    truck_range = 500
    mpg = 10

    # Logic: Finding the cheapest station globally to use for segments
    # (Aap isse geometry-based bhi kar sakte hain future mein)
    cheapest_row = df.loc[df['Retail Price'].idxmin()]
    avg_price = float(cheapest_row['Retail Price'])

    while miles_covered < total_miles:
        # Destination check
        if (total_miles - miles_covered) <= truck_range:
            remaining_miles = total_miles - miles_covered
            total_cost += (remaining_miles / mpg) * avg_price
            break

        # Add a stop every 500 miles
        stop_info = {
            "station": str(cheapest_row['Truckstop Name']),
            "city": str(cheapest_row['City']),
            "state": str(cheapest_row['State']),
            "price_per_gallon": round(avg_price, 2),
            "miles_at_stop": round(miles_covered + truck_range, 2)
        }
        fuel_stops.append(stop_info)
        
        total_cost += (truck_range / mpg) * avg_price
        miles_covered += truck_range

    return fuel_stops, round(total_cost, 2)