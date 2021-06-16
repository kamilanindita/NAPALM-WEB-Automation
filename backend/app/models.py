from djongo import models

class Device(models.Model):
    id_device=models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    type_device= models.CharField(max_length=50)
    network_driver = models.CharField(max_length=10)
    optional_args = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.id_device)

class DeviceInformation(models.Model):
    id=models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, related_name="informations",)
    fqdn = models.CharField(blank=True, max_length=50)
    hostname = models.CharField(blank=True, max_length=50)
    interfaces_list = models.TextField(blank=True)
    model = models.CharField(blank=True, max_length=50)
    os_version = models.TextField(blank=True)
    serial_number = models.CharField(blank=True, max_length=50)
    uptime = models.CharField(blank=True, max_length=50)
    vendor = models.CharField(blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.device)

class DeviceInterface(models.Model):
    id=models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, null=True, related_name="interfaces",)
    name = models.CharField(blank=True, max_length=50)
    description = models.CharField(blank=True, max_length=150)
    is_enabled = models.BooleanField()
    is_up = models.BooleanField()
    mac_address = models.CharField(blank=True, max_length=50)
    mtu = models.CharField(blank=True, max_length=50)
    speed = models.CharField(blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.device)

class DeviceArp(models.Model):
    id=models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, related_name="arp",)
    interface = models.CharField(blank=True, max_length=50)
    mac = models.CharField(blank=True, max_length=50)
    ip = models.CharField(blank=True, max_length=50)
    age = models.CharField(blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.device)

class DeviceBackup(models.Model):
    id=models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, related_name="backups")
    backup = models.TextField(blank=True)
    filename = models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return "{}".format(self.device)

class DeviceRestore(models.Model):
    id=models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, related_name="restores")
    restore = models.TextField(blank=True)
    compare = models.TextField(blank=True)
    before = models.TextField(blank=True)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.device)


class DeviceLogConfiguration(models.Model):
    id=models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, related_name="configs")
    config = models.TextField()
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return "{}".format(self.device)