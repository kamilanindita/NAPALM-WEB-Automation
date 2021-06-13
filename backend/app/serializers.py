from rest_framework import serializers
from app.models import Device, DeviceInformation, DeviceInterface, DeviceArp, DeviceLogConfiguration, DeviceBackup, DeviceRestore
from datetime import datetime

#Device------------------------------------------------------------------------------------------------------------------------------------
class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    informations = serializers.HyperlinkedIdentityField(view_name='deviceinformation-detail', read_only=True)
    interfaces = serializers.HyperlinkedIdentityField(view_name='deviceinterface-detail', read_only=True)
    arp = serializers.HyperlinkedIdentityField(view_name='devicearp-detail', read_only=True)

    class Meta:
        model = Device
        fields = ['url','id_device','ip_address','username', 'password', 'type_device', 'network_driver', 'optional_args','informations','interfaces','arp','created_at','updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

class DeviceMiniSerializer(serializers.Serializer):
    value = serializers.CharField(source='id_device')
    label = serializers.SerializerMethodField()
    ip = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['value','label','ip']

    def get_label(self, obj):
        ip_address=''
        hostname=''
        queryset=DeviceInformation.objects.filter(device=obj.id_device)
        if queryset:
            ip_address=obj.ip_address
            hostname=queryset[0].hostname

        return  hostname+' - '+ip_address

    def get_ip(self, obj):
        ip_address=''
        queryset=DeviceInformation.objects.filter(device=obj.id_device)
        if queryset:
            ip_address=obj.ip_address
 
        return  ip_address

class AddDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__' 

class DeviceSummarySerializer(serializers.HyperlinkedModelSerializer):
    devices =  serializers.SerializerMethodField()
    success_task =  serializers.SerializerMethodField()
    failed_task = serializers.SerializerMethodField()
    system =  serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['devices','success_task','failed_task','system']

    def get_devices(self, obj):
        return Device.objects.all().count()
        
    def get_success_task(self, obj):
        return DeviceLogConfiguration.objects.filter(status='success').count()

    def get_failed_task(self, obj):
        return DeviceLogConfiguration.objects.filter(status='failed').count()

    def get_system(self, obj): 
        curr_date = datetime.now()
        date=curr_date.strftime("%c")

        return date

#End Device--------------------------------------------------------------------------------------------------------------------------------


#Device Information------------------------------------------------------------------------------------------------------------------------
class DeviceInformationSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.SlugRelatedField(
        read_only=False,
        queryset=Device.objects.all(),
        slug_field='id_device'
    )

    interfaces_list=serializers.JSONField()

    class Meta:
        model = DeviceInformation
        fields = ['device','fqdn','hostname', 'interfaces_list', 'model', 'os_version', 'serial_number', 'uptime','vendor','created_at']    

#End Device Information--------------------------------------------------------------------------------------------------------------------


#Device Interfaces-------------------------------------------------------------------------------------------------------------------------
class DeviceInterfaceSerializer(serializers.ModelSerializer):
    device = serializers.SlugRelatedField(
        read_only=False,
        queryset=Device.objects.all(),
        slug_field='id_device'
    )

    class Meta:
        model = DeviceInterface
        fields = ['device','name','is_enabled','is_up','description','mac_address','mtu','speed'] 

#End Device Interfaces---------------------------------------------------------------------------------------------------------------------


#Device Arp--------------------------------------------------------------------------------------------------------------------------------
class DeviceArpSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.SlugRelatedField(
        read_only=False,
        queryset=Device.objects.all(),
        slug_field='id_device'
    )

    class Meta:
        model = DeviceArp
        fields = ['device','interface','mac','ip','age'] 

#End Device Arp----------------------------------------------------------------------------------------------------------------------------


#Device Backup-----------------------------------------------------------------------------------------------------------------------------
class DeviceBackupListSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.ReadOnlyField(source='device.id_device')
    devices = serializers.SerializerMethodField()

    class Meta:
        model = DeviceBackup
        fields = ['device_id','devices','backup','filename','status','created_at']

    def get_devices(self, obj):
        ip=''
        host=''
        vendor=''
        queryset=DeviceInformation.objects.filter(device=obj.device_id)
        query_ip=Device.objects.filter(id_device=obj.device_id)
        if queryset:
            ip=query_ip[0].ip_address
            host=queryset[0].hostname
            vendor=queryset[0].vendor

        return 'IP Address:'+ip+', Hostname:'+host+', Vendor:'+vendor

class DeviceBackupSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.SlugRelatedField(
        read_only=False,
        queryset=Device.objects.all(),
        slug_field='id_device'
    )

    class Meta:
        model = DeviceBackup
        fields = ['device','backup','filename','status','created_at']

#End Device Backup-------------------------------------------------------------------------------------------------------------------------


#Device Restore----------------------------------------------------------------------------------------------------------------------------
class DeviceRestoreListSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.ReadOnlyField(source='device.id_device')
    devices = serializers.SerializerMethodField()

    class Meta:
        model = DeviceRestore
        fields = ['device_id','devices','restore','status','created_at']

    def get_devices(self, obj):
        ip=''
        host=''
        vendor=''
        queryset=DeviceInformation.objects.filter(device=obj.device_id)
        query_ip=Device.objects.filter(id_device=obj.device_id)
        if queryset:
            ip=query_ip[0].ip_address
            host=queryset[0].hostname
            vendor=queryset[0].vendor

        return 'IP Address:'+ip+', Hostname:'+host+', Vendor:'+vendor

class DeviceRestoreSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.SlugRelatedField(
        read_only=False,
        queryset=Device.objects.all(),
        slug_field='id_device'
    )

    class Meta:
        model = DeviceRestore
        fields = ['device','restore','compare','before','status','created_at']

#End Device Restore------------------------------------------------------------------------------------------------------------------------


#Device Log Configuration------------------------------------------------------------------------------------------------------------------
class DeviceLogConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.SlugRelatedField(
        read_only=False,
        queryset=Device.objects.all(),
        slug_field='id_device'
    )


    class Meta:
        model = DeviceLogConfiguration
        fields = ['device','config','status', 'created_at']
       
class DeviceLogConfigurationListSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.ReadOnlyField(source='device.id_device')
    devices = serializers.SerializerMethodField()
    
    class Meta:
        model = DeviceLogConfiguration
        fields = ['device_id','devices','config','status', 'created_at']
        
    def get_devices(self, obj):
        ip=''
        host=''
        vendor=''
        queryset=DeviceInformation.objects.filter(device=obj.device_id)
        query_ip=Device.objects.filter(id_device=obj.device_id)
        if queryset:
            ip=query_ip[0].ip_address
            host=queryset[0].hostname
            vendor=queryset[0].vendor

        return  'IP Address:'+ip+', Hostname:'+host+', Vendor:'+vendor

#End Device Log Configuration--------------------------------------------------------------------------------------------------------------


