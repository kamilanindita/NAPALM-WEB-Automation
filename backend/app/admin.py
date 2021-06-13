from django.contrib import admin
from app.models import Device, DeviceInformation, DeviceInterface, DeviceArp, DeviceLogConfiguration, DeviceBackup, DeviceRestore

# Register your models here.
admin.site.register(Device)
admin.site.register(DeviceInformation)
admin.site.register(DeviceInterface)
admin.site.register(DeviceArp)
admin.site.register(DeviceLogConfiguration)
admin.site.register(DeviceBackup)
admin.site.register(DeviceRestore)
