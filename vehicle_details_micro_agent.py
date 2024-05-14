import http.client
import json

# Replace with your RapidAPI key
RAPIDAPI_KEY = 'c6f2160b1amsha84b1fe7aeba5edp143b2djsn849e7dbe7338'

# Function to get vehicle details
def get_vehicle_details(vehicle_number):
    conn = http.client.HTTPSConnection("rto-vehicle-information-verification-india.p.rapidapi.com")
    
    payload = json.dumps({
        "reg_no": vehicle_number,
        "consent": "Y",
        "consent_text": "I hereby declare my consent agreement for fetching my information via AITAN Labs API"
    })
    
    headers = {
        'content-type': "application/json",
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': "rto-vehicle-information-verification-india.p.rapidapi.com"
    }
    
    conn.request("POST", "/api/v1/rc/vehicleinfo", payload, headers)
    
    res = conn.getresponse()
    data = res.read()
    
    return data.decode("utf-8")

# Main function
if __name__ == "__main__":
    vehicle_number = input("Enter the vehicle number: ")
    vehicle_details = get_vehicle_details(vehicle_number)
    print("Vehicle Details:")
    print(vehicle_details)
