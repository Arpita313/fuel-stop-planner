import os
import pandas as pd
import requests

def get_route(start_coords, finish_coords):
    # Dashbaord se copy ki hui key
    api_key = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjAxNTQ5YWQ1ZDE5MDQyYjZiNTkxN2Q4YjMwMDNjMDA1IiwiaCI6Im11cm11cjY0In0='
    
    # Heigit wala domain hata kar wapas stable openrouteservice use karein
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_coords}&end={finish_coords}"
    
    try:
        response = requests.get(url)
        # Agar response JSON nahi hai, toh crash nahi hoga
        if response.status_code != 200:
            return None, 0
            
        data = response.json()
        geometry = data['features'][0]['geometry']['coordinates']
        dist_meters = data['features'][0]['properties']['summary']['distance']
        return geometry, dist_meters / 1609.34 # Meters to Miles
    except:
        return None, 0

def calculate_fuel_plan(total_miles):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'fuel-prices.csv')
    
    df = pd.read_csv(csv_path)
    # CSV columns match: 'Truckstop Name' and 'Retail Price'
    df['Retail Price'] = pd.to_numeric(df['Retail Price'], errors='coerce')
    cheapest_row = df.loc[df['Retail Price'].idxmin()]
    
    price = float(cheapest_row['Retail Price'])
    total_cost = (total_miles / 10) * price # 10 MPG logic
    
    stop_info = {
        "station": str(cheapest_row['Truckstop Name']),
        "city": str(cheapest_row['City']),
        "state": str(cheapest_row['State']),
        "price_per_gallon": round(price, 2)
    }
    return [stop_info], round(total_cost, 2)