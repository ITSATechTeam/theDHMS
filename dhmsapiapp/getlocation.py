import requests
import json

# Get user location considering their IP address
def get_user_location(api_key):
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + api_key
    data = {
        "considerIp": "true"
    }
    
    response = requests.post(url, json=data)
    location_data = response.json()
    
    if 'location' in location_data:
        latitude = location_data['location']['lat']
        longitude = location_data['location']['lng']
        accuracy = location_data['accuracy']  # Accuracy in meters
        return latitude, longitude, accuracy
    else:
        return None


# call 'get_user_location' function
# Replace with your Google Maps API key
# api_key = "YOUR_GOOGLE_MAPS_API_KEY"
# location = get_user_location(api_key)

# if location:
#     latitude, longitude, accuracy = location
#     print(f"Latitude: {latitude}, Longitude: {longitude}, Accuracy: {accuracy} meters")
# else:
#     print("Unable to determine the user's location")


# Get current users location using their latitude and longitude
def get_address_from_coordinates(latitude, longitude):
    try:
        api_key = 'AIzaSyCT-K1SWR7r3HNcaV_n8IS7XGFf4_2TBnw'
        # url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?{api_key}"
        # https://maps.googleapis.com/maps/api/geocode/json?latlng=lat,lng&key=YOUR_API_KEY

        
        response = requests.get(url)
        address_data = response
        # address_data = response.json()
        print(address_data)
        # print(address)
        
        if 'results' in address_data and len(address_data['results']) > 0:
            address = address_data['results'][0]['formatted_address']
            print(address)
            return address
        else:
            return "Address not found"
    except:
        return "Address not found"


# call 'get_address_from_coordinates' function
# # Convert latitude and longitude to address
# if location:
#     address = get_address_from_coordinates(latitude, longitude)
#     print(f"Address: {address}")


# Determin location using longitude and latitude without Google maps API
def get_location_from_lat_long(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse"    
    # Parameters for the API
    params = {
        'lat': latitude,
        'lon': longitude,
        'format': 'geocodejson'
        # 'format': 'json'  # You can also use 'xml' or 'html'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            if 'features' in data and data['features']:
                # print(features)
                address = data['features'][0]['properties']['geocoding']
                print(address)
                if address == 'No address found':
                    return "Address not found"                
                return address
            else:
                return "Address not found"
            
        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to decode the response as JSON.")
            return 'Address not found'
    else:
        return 'Location could not be found'




# START OF FINDING LOCATION USING A PYTHON PACKAGE
from geopy.geocoders import OpenCage

def get_location_from_lat_long_opencage(latitude, longitude):
    api_key = '7330da1295114996b84123c3d080baac'
    geolocator = OpenCage(api_key)
    
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        return location.address if location else "No address found"
    except Exception as e:
        return f"Error: {e}"

# # Example usage
# latitude = 37.7749
# longitude = -122.4194
# api_key = 'YOUR_OPENCAGE_API_KEY'  # You need an API key for OpenCage

# location = get_location_from_lat_long_opencage(latitude, longitude, api_key)
# print(location)

# END OF FINDING LOCATION USING A PYTHON PACKAGE




# GET LOCATION WITH IP WITHOUT GOOGLE MAPS
def get_location_from_ip():
    url = 'https://ipinfo.io'
    
    response = requests.get(url)
    data = response.json()

    # The data will include location information based on the user's IP
    location = data.get("loc", None)  # The "loc" field contains latitude and longitude
    if location:
        latitude, longitude = map(float, location.split(','))
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        return latitude, longitude
    else:
        return "Location not found"

# location = get_location_from_ip()
# print(location)
