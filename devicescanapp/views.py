from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, schema
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def StartApp(request):
    print('App ran successfully')
    
    
from django.http import JsonResponse
from .models import DeviceLocation, InstalledApplication



# @swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['POST'])
def save_applications(request):
    print('save_applications funtion called successfully')
    if request.method == "POST":
        data = request.POST.get("applications", [])
        deviceHealthData = request.POST.get("deviceHealthInfo", [])
        # print('deviceHealthData')
        # print(deviceHealthData)
        deviceHealthDataProcessed = json.loads(deviceHealthData)
        deviceLocationCountry = deviceHealthDataProcessed['deviceLocationCountry']
        deviceLocationRegion = deviceHealthDataProcessed['deviceLocationRegion']
        deviceLocationCity = deviceHealthDataProcessed['deviceLocationCity']
        deviceLocationLatitude = deviceHealthDataProcessed['deviceLocationLatitude']
        deviceLocationLongitude = deviceHealthDataProcessed['deviceLocationLongitude']
        deviceLocationISP = deviceHealthDataProcessed['deviceLocationISP']
        deviceIPAddress = deviceHealthDataProcessed['deviceIPAddress']
        deviceMacAddress = deviceHealthDataProcessed['deviceMacAddress']
        deviceRamSize = deviceHealthDataProcessed['Device Info']['RAM Size (GB)']
        deviceCPUUsage = deviceHealthDataProcessed['CPU Usage (%)']
        deviceCPUCores = deviceHealthDataProcessed['Device Info']['CPU Cores']
        deviceOS = deviceHealthDataProcessed['Device Info']['Operating System']
        deviceOSVersion = deviceHealthDataProcessed['Device Info']['OS Version']
        deviceArchitecture = deviceHealthDataProcessed['Device Info']['Architecture']
        deviceDeviceName = deviceHealthDataProcessed['Device Info']['Device Name']
        deviceTotalMemoryGB = deviceHealthDataProcessed['Memory Usage']['Total Memory (GB)']
        deviceUsedMemoryGB = deviceHealthDataProcessed['Memory Usage']['Used Memory (GB)']
        deviceMemoryUsagePecentage = deviceHealthDataProcessed['Memory Usage']['Memory Usage (%)']
        deviceTotalDiskGB = deviceHealthDataProcessed['Disk Usage']['Total Disk (GB)']
        deviceUsedDiskGB = deviceHealthDataProcessed['Disk Usage']['Used Disk (GB)']
        deviceDiskUsagePercentage = deviceHealthDataProcessed['Disk Usage']['Disk Usage (%)']
        deviceBatteryPercentage = deviceHealthDataProcessed['Battery Status']['Battery Percentage']
        deviceBatteryChargingStatus = deviceHealthDataProcessed['Battery Status']['Charging']
        deviceUpTimePeriod = deviceHealthDataProcessed['System Uptime']
        
        # save device health data to DB
        DeviceHealth.objects.create(
            device_name = deviceDeviceName, 
            operating_system = deviceOS,
            cpu_usage = deviceCPUUsage,
            ram_size = deviceRamSize,
            cpu_cores = deviceCPUCores,
            operating_system_version = deviceOSVersion,
            device_architecture = deviceArchitecture,
            total_memory = deviceTotalMemoryGB,
            used_memory = deviceUsedMemoryGB,
            memory_usage = deviceMemoryUsagePecentage,
            total_disk = deviceTotalDiskGB,
            used_disk = deviceUsedDiskGB,
            disk_usage = deviceDiskUsagePercentage,
            battery_percentage = deviceBatteryPercentage,
            is_charging = deviceBatteryChargingStatus,
            system_uptime = deviceUpTimePeriod,
            ip_address = deviceIPAddress,
            mac_address = deviceMacAddress,
            )
        
        DeviceLocation.objects.create(
            device_name = deviceDeviceName,
            operating_system = deviceOS,
            latitude = deviceLocationLatitude,
            longitude = deviceLocationLongitude,
            city = deviceLocationCity,
            region = deviceLocationRegion,
            country = deviceLocationCountry,
            deviceLocationISP = deviceLocationISP,
            ip_address = deviceIPAddress,
            mac_address = deviceMacAddress
        )

        # Convert data to a list if it's a string
        applications = eval(data) if isinstance(data, str) else data
        for app in applications:
            InstalledApplication.objects.create(
                # name=app,
                name=app.get("name"),
                ip_address=app.get("deviceIPAddress"),
                mac_address=app.get("deviceMacAddress"),
                installed_date=app.get("installed_date"),
                device_name=app.get("deviceName"),
                # device_name=device_name
            )

        return JsonResponse({"message": "Applications saved successfully"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=400)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import DeviceHealth

@csrf_exempt
def saveDeviceHealthInfo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            DeviceHealth.objects.create(
                user_id=data['user_id'],  # Replace with the authenticated user's ID
                device_name=data['Device Info']['Device Name'],
                operating_system=data['Device Info']['Operating System'],
                cpu_usage=data['CPU Usage (%)'],
                total_memory=data['Memory Usage']['Total Memory (GB)'],
                used_memory=data['Memory Usage']['Used Memory (GB)'],
                memory_usage=data['Memory Usage']['Memory Usage (%)'],
                total_disk=data['Disk Usage']['Total Disk (GB)'],
                used_disk=data['Disk Usage']['Used Disk (GB)'],
                disk_usage=data['Disk Usage']['Disk Usage (%)'],
                battery_percentage=data['Battery Status']['Battery Percentage'],
                is_charging=data['Battery Status']['Charging'],
                system_uptime=data['System Uptime']
            )
            return JsonResponse({"status": "success", "message": "Device health data saved."}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
