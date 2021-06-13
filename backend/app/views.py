from app.models import Device, DeviceInformation, DeviceInterface, DeviceArp, DeviceLogConfiguration, DeviceBackup, DeviceRestore
from app.serializers import DeviceSummarySerializer, AddDeviceSerializer, DeviceSerializer, DeviceMiniSerializer, DeviceInformationSerializer, DeviceInterfaceSerializer, DeviceArpSerializer, DeviceLogConfigurationListSerializer, DeviceLogConfigurationSerializer, DeviceBackupListSerializer, DeviceBackupSerializer, DeviceRestoreListSerializer
from app.paginations import DeviceListPagination, ConfigurationListPagination, RecentConfigurationListPagination, BackupRestoreConfigurationListPagination
import json
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from app.modules import Modules
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import datetime
import os


#Summary-----------------------------------------------------------------------------------------------------------------
class DeviceSummary(generics.ListAPIView):
    permission_classes= [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSummarySerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DeviceSummarySerializer(queryset, many=False)
        return Response(serializer.data)

#End Summary--------------------------------------------------------------------------------------------------------------


#Test Connection----------------------------------------------------------------------------------------------------------
class TestConnection(APIView):
    #permission_classes= [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id=self.kwargs['pk']
        try:
            device=Device.objects.filter(id_device=id)          
            status = Modules.get_connection(device[0].ip_address)
            result= { 'ip_address':device[0].ip_address, 'connection':status }
            return Response(result)
        except:
            result= {'device not found'}
            return Response(result)

    def post(self, request, format=None):
        status = Modules.get_connection(self.request.data['ip_address'])
        result= { 'ip_address':request.data['ip_address'], 'connection':status }
        return Response(result)

#End Test Connection------------------------------------------------------------------------------------------------------


# Device------------------------------------------------------------------------------------------------------------------
class ConvertToObject(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

class DeviceMiniList(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceMiniSerializer
    pagination_class=None


class DeviceList(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = DeviceListPagination

    def create(self, request, *args, **kwargs):
        serializer=AddDeviceSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data)
            device_detail=serializer.data
            device=json.dumps(device_detail)
            device=ConvertToObject(device)
            result=Modules.get_informations(device)
            if result:
                data={'device':device.id_device,'fqdn':result['fqdn'],'hostname':result['hostname'],'interfaces_list':result['interface_list'],'model':result['model'],'os_version':result['os_version'],'serial_number':str(result['serial_number']),'uptime':result['uptime'],'vendor':result['vendor']}
                serializer = DeviceInformationSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"device":device_detail,"information":serializer.data})
                return Response({"device":device_detail,"information":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

#End Device---------------------------------------------------------------------------------------------------------------


#Device Information-------------------------------------------------------------------------------------------------------
#information device
class DeviceInformationDetailLatest(generics.RetrieveAPIView):
    permission_classes= [IsAuthenticated]
    queryset = DeviceInformation.objects.all()
    serializer_class = DeviceInformationSerializer

    def get_object(self, *args, **kwargs):
        id_device=self.kwargs['pk']
        try:
            return DeviceInformation.objects.filter(device=id_device).latest('created_at')
        except DeviceInformation.DoesNotExist:
            return False

    def retrieve(self, request, *args, **kwargs):
        id_device=self.kwargs['pk']
        self.object = self.get_object()
        if self.object:
            serializer = self.get_serializer(self.object)
            return Response(serializer.data)
        else:
            device = Device.objects.filter(id_device=id_device)
            if device:
                return Response('get otomatisasi',status.HTTP_404_NOT_FOUND)
            return Response('device not found',status.HTTP_404_NOT_FOUND)

#information synchronos
class DeviceInformationSynchronos(APIView):

    def get_object(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False
       
    def get_object_information(self, pk):
        try:
            return DeviceInformation.objects.filter(device=pk)
        except DeviceInterface.DoesNotExist:
            return False

    def get(self, request, pk, format=None):
        device = self.get_object(pk)
        if device:
            result=Modules.get_informations(device[0])
            if result=='Cannot connect to device':
                data_result={"device":pk,"message":result,"status":"failed"}
                return Response(data_result)

            elif result:
                device_information=self.get_object_information(pk)
                device_information.delete()

                data={'device':pk,'fqdn':result['fqdn'],'hostname':result['hostname'],'interfaces_list':result['interface_list'],'model':result['model'],'os_version':result['os_version'],'serial_number':str(result['serial_number']),'uptime':result['uptime'],'vendor':result['vendor']}
                serializer = DeviceInformationSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response('data information not found',status.HTTP_404_NOT_FOUND)
        return Response('device not found',status.HTTP_404_NOT_FOUND)

#End Device Information---------------------------------------------------------------------------------------------------


#Device Interface---------------------------------------------------------------------------------------------------------
#interface list name
class DeviceInterfaceName(generics.ListAPIView):
    permission_classes= [IsAuthenticated]
    # queryset = DeviceInterface.objects.all()
    serializer_class = DeviceInterfaceSerializer

    def get_queryset(self):
        id_device=self.kwargs['pk']
        try:
            return DeviceInterface.objects.filter(device=id_device)
        except DeviceInterface.DoesNotExist:
            return False

    def list(self, request, *args, **kwargs):
        id_device=self.kwargs['pk']
        queryset = self.get_queryset() 
        list=[]
        for data in queryset:
            list.append(data.name)

        return Response(list)

#interface table
class DeviceInterfaceDetail(generics.ListAPIView):
    permission_classes= [IsAuthenticated]
    # queryset = DeviceInterface.objects.all()
    serializer_class = DeviceInterfaceSerializer

    def get_object_device(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def get_queryset(self):
        id_device=self.kwargs['pk']
        try:
            return DeviceInterface.objects.filter(device=id_device)
        except DeviceInterface.DoesNotExist:
            return False

    def list(self, request, *args, **kwargs):
        id_device=self.kwargs['pk']
        queryset = self.get_queryset() 
        if queryset:
            serializer =DeviceInterfaceSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            device = self.get_object_device(id_device)
            if device:
                result=Modules.get_interfaces(device[0])
                Data=[]
                if result:
                    for data in result:
                        try:
                            mtu=result[data]["mtu"]
                        except KeyError:
                            mtu=''

                        data_result={"device":id_device,"name":data,"is_enabled":result[data]["is_enabled"],"is_up":result[data]["is_up"],"description":result[data]["description"],"mac_address":result[data]['mac_address'],"mtu":mtu,"speed":result[data]["speed"]}
                        serializer = DeviceInterfaceSerializer(data=data_result)
                        if serializer.is_valid():
                            serializer.save()
                        Data.append(serializer.data)
                    return Response(Data)
                return Response('data interfaces not found',status.HTTP_404_NOT_FOUND)
            return Response('device not found',status.HTTP_404_NOT_FOUND)
                   
#interface synchronos
class DeviceInterfaceSynchronos(APIView):

    def get_object(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def get_object_interface(self, pk):
        try:
            return DeviceInterface.objects.filter(device=pk)
        except DeviceInterface.DoesNotExist:
            return False

    def get(self, request, pk, format=None):
        device = self.get_object(pk)
        if device:
            result=Modules.get_interfaces(device[0])
            Data=[]
            if result=='Cannot connect to device':
                data_result={"device":pk,"message":result,"status":"failed"}
                return Response(data_result)

            elif result:
                device_interfaces=self.get_object_interface(pk)
                device_interfaces.delete()
                for data in result:
                    try:
                        mtu=result[data]["mtu"]
                    except KeyError:
                        mtu=''

                    data_result={"device":pk,"name":data,"is_enabled":result[data]["is_enabled"],"is_up":result[data]["is_up"],"description":result[data]["description"],"mac_address":result[data]['mac_address'],"mtu":mtu,"speed":result[data]["speed"]}
                    serializer = DeviceInterfaceSerializer(data=data_result)
                    if serializer.is_valid():
                        serializer.save()
                    Data.append(data_result)
                return Response(Data)
            return Response('data interfaces not found',status.HTTP_404_NOT_FOUND)
        return Response('device not found',status.HTTP_404_NOT_FOUND)
#End Device Interfaces----------------------------------------------------------------------------------------------------


#Device Arp---------------------------------------------------------------------------------------------------------------
#ARP table
class DeviceArpDetail(generics.ListAPIView):
    permission_classes= [IsAuthenticated]
    # queryset = DeviceArp.objects.all()
    serializer_class = DeviceArpSerializer

    def get_object_device(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def get_queryset(self):
        id_device=self.kwargs['pk']
        try:
            return DeviceArp.objects.filter(device=id_device)
        except DeviceArp.DoesNotExist:
            return False

    def list(self, request, *args, **kwargs):
        id_device=self.kwargs['pk']
        queryset = self.get_queryset() 
        if queryset:
            serializer =DeviceArpSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            device = self.get_object_device(id_device)
            if device:
                result=Modules.get_arp_tables(device[0])
                Data=[]
                if result:
                    for data in result:
                        data_result={"device":id_device,"interface":data["interface"],"mac":data["mac"],"ip":data["ip"],"age":data["age"]}
                        serializer = DeviceArpSerializer(data=data_result)
                        if serializer.is_valid():
                            serializer.save()
                        Data.append(serializer.data)
                    return Response(Data)
                return Response('data arp not found',status.HTTP_404_NOT_FOUND)
            return Response('device not found',status.HTTP_404_NOT_FOUND)

#ARP Synchronos
class DeviceArpSynchronos(APIView):

    def get_object(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def get_object_arp(self, pk):
        try:
            return DeviceArp.objects.filter(device=pk)
        except DeviceArp.DoesNotExist:
            return False

    def get(self, request, pk, format=None):
        device = self.get_object(pk)
        if device:
            result=Modules.get_arp_tables(device[0])
            Data=[]
            #result=str(result)
            if result=='Cannot connect to device':
                data_result={"device":pk,"message":result,"status":"failed"}
                return Response(data_result)

            elif result:
                device_arp=self.get_object_arp(pk)
                device_arp.delete()
                for data in result:
                    data_result={"device":pk,"interface":data["interface"],"mac":data["mac"],"ip":data["ip"],"age":data["age"]}
                    serializer = DeviceArpSerializer(data=data_result)
                    if serializer.is_valid():
                        serializer.save()
                    Data.append(serializer.data)
                return Response(Data)
            return Response('data arp table not found',status.HTTP_404_NOT_FOUND)
        return Response('device not found',status.HTTP_404_NOT_FOUND)

#End Device Arp-----------------------------------------------------------------------------------------------------------


#Device Backup Configuration----------------------------------------------------------------------------------------------
#backup all list
class BackupConfigurationList(generics.ListCreateAPIView):
    #permission_classes= [IsAuthenticated]
    queryset = DeviceBackup.objects.all().order_by('-created_at')
    serializer_class = DeviceBackupListSerializer
    pagination_class = BackupRestoreConfigurationListPagination

#run backup
class BackupConfiguration(generics.RetrieveAPIView):
    queryset = DeviceBackup.objects.all()
    serializer_class = DeviceBackupSerializer

    def get_object(self, *args, **kwargs):
        id_device=self.kwargs['pk']
        try:
            return Device.objects.filter(id_device=id_device)
        except Device.DoesNotExist:
            return False

    def retrieve(self, request, *args, **kwargs):
        id_device=self.kwargs['pk']
        device = self.get_object()
        if device:
            result=Modules.run_backup(id_device, device[0])
            curr_date = datetime.now()
            date=curr_date.isoformat()

            if result!='Cannot connect to device':
                dirname = os.path.dirname(__file__)
                label=device[0].ip_address+"_"+date+".txt"
                filename = os.path.join(dirname, "../backup/"+label)
                
                f = open(filename, "w")
                f.write(str(result))
                f.close()

                data_result={"device":id_device,"backup":result,"filename":label,"status":"success","created_at":date}
                serializer = DeviceBackupSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
 
                return Response(serializer.data)

            elif result=='Cannot connect to device':
                data_result={"device":id_device,"backup":result,"status":"failed","created_at":date}
                serializer = DeviceBackupSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
 
                return Response(serializer.data)
            else:
                return Response('data acl not found',status.HTTP_404_NOT_FOUND)

        return Response('device not found',status.HTTP_404_NOT_FOUND)

#End Device Backup Configuration------------------------------------------------------------------------------------------


#Device Restore Configuration---------------------------------------------------------------------------------------------
#restore all list
class RestoreConfigurationList(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    queryset = DeviceRestore.objects.all().order_by('-created_at')
    serializer_class = DeviceRestoreListSerializer
    pagination_class = BackupRestoreConfigurationListPagination

#run restore
class RestoreConfiguration(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        id_device=self.kwargs['pk']
        file=request.data['file']
        result=Modules.run_restore(id_device, file)
        if result:
            return Response(result)
        return Response('failed',status.HTTP_404_NOT_FOUND)
        #return Response('device not found',status.HTTP_404_NOT_FOUND)

#End Device Restore Configuration-----------------------------------------------------------------------------------------


#Device Log Configuration-------------------------------------------------------------------------------------------------
#get all configuration
class LogConfigurationList(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    queryset = DeviceLogConfiguration.objects.all().order_by('-created_at')
    serializer_class = DeviceLogConfigurationListSerializer
    pagination_class = ConfigurationListPagination

#get recent configuration
class RecentConfigurationList(generics.ListAPIView):
    permission_classes= [IsAuthenticated]
    queryset = DeviceLogConfiguration.objects.all().order_by('-created_at')
    serializer_class = DeviceLogConfigurationListSerializer
    pagination_class = RecentConfigurationListPagination

#End Device Log Configuration---------------------------------------------------------------------------------------------


#Configuration Existing---------------------------------------------------------------------------------------------------
class ConfigurationExisting(APIView):
    permission_classes= [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def get(self, request, pk, format=None):
        device = self.get_object(pk)
        if device:
            result=Modules.get_existing_configuration(device[0])
            if result:
                return Response({"id_device":pk,"existing":result})
            return Response('data configuration not found',status.HTTP_404_NOT_FOUND)
        return Response('device not found',status.HTTP_404_NOT_FOUND)

#End Configuration Existing-----------------------------------------------------------------------------------------------


#Run Configuration--------------------------------------------------------------------------------------------------------
#running acl ipv4 configuration
class RunConfiguration(APIView):
    def get_object(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def post(self, request, *args, **kwargs):
        device=self.get_object(self.kwargs['pk'])
        if device:
            result=Modules.run_configuration(device[0], self.request.data)
            serializer = DeviceLogConfigurationSerializer(data=result)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

            return Response('device not found',status.HTTP_404_NOT_FOUND)

#running acl ipv6 configuration
class RunConfigurationIPv6(APIView):
    def get_object(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def post(self, request, *args, **kwargs):
        device=self.get_object(self.kwargs['pk'])
        print(self.request.data)
        if device:
            result=Modules.run_configuration_ipv6(device[0], self.request.data)
            serializer = DeviceLogConfigurationSerializer(data=result)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

            return Response('device not found',status.HTTP_404_NOT_FOUND)

#Run Configuration--------------------------------------------------------------------------------------------------------


#Run CLI Configuration----------------------------------------------------------------------------------------------------
class RunCLIConfiguration(APIView):
    def get_object(self, pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False

    def post(self, request, *args, **kwargs):
        device=self.get_object(self.kwargs['pk'])
        if device:
            result=Modules.run_cli_configuration(device[0], self.request.data)
            serializer = DeviceLogConfigurationSerializer(data=result)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response('device not found',status.HTTP_404_NOT_FOUND)

#End CLI Configuration----------------------------------------------------------------------------------------------------
