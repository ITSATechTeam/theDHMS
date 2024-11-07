# LOCATION DETERMINATION
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Replace with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = 'your_google_maps_api_key'

@csrf_exempt
def get_location_from_coordinates(request):
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is None or longitude is None:
                return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)

            # Call Google Maps Geocoding API
            response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_MAPS_API_KEY}')
            response_data = response.json()

            # Check if the response contains results
            if response_data['status'] == 'OK' and len(response_data['results']) > 0:
                # Extract the formatted address (location name)
                location_name = response_data['results'][0]['formatted_address']
                return JsonResponse({'location_name': location_name}, status=200)
            else:
                return JsonResponse({'error': 'Location not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
