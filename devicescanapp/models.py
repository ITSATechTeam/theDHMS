from django.db import models

# Create your models here.
from django.db import models

class InstalledApplication(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=100, null=True, blank=True)
    mac_address = models.CharField(max_length=100, null=True, blank=True)
    installed_date = models.DateField(null=True, blank=True)
    device_name = models.CharField(max_length=255, null=True, blank=True) 

    def __str__(self):
        return self.name


from django.db import models

class DeviceHealth(models.Model):
    device_name = models.CharField(max_length=255)
    operating_system = models.CharField(max_length=100)
    ram_size = models.CharField(max_length=100, null=True, blank=True)
    operating_system_version = models.CharField(max_length=100, null=True, blank=True)
    device_architecture = models.CharField(max_length=100, null=True, blank=True)
    cpu_usage = models.CharField(max_length=100, null=True, blank=True)
    cpu_cores = models.CharField(max_length=100, null=True, blank=True)
    total_memory = models.CharField(max_length=100, null=True, blank=True)
    used_memory = models.CharField(max_length=100, null=True, blank=True)
    memory_usage = models.CharField(max_length=100, null=True, blank=True)
    total_disk = models.CharField(max_length=100, null=True, blank=True)
    used_disk = models.CharField(max_length=100, null=True, blank=True)
    disk_usage = models.CharField(max_length=100, null=True, blank=True)
    battery_percentage = models.CharField(max_length=100, null=True, blank=True)
    is_charging = models.BooleanField(null=True, blank=True)
    system_uptime = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=100, null=True, blank=True)
    mac_address = models.CharField(max_length=100, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_name} - {self.recorded_at}"


class DeviceLocation(models.Model):
    device_name = models.CharField(max_length=255)
    operating_system = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=100, null=True, blank=True)
    deviceLocationISP = models.CharField(max_length=100, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_name} - {self.recorded_at}"
