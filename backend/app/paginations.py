from rest_framework import pagination

class DeviceListPagination(pagination.PageNumberPagination):       
       page_size = 10

class ConfigurationListPagination(pagination.PageNumberPagination):       
       page_size = 10

class RecentConfigurationListPagination(pagination.PageNumberPagination):       
       page_size = 5

class BackupRestoreConfigurationListPagination(pagination.PageNumberPagination):       
       page_size = 5