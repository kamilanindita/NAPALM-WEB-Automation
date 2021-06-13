
function getDevices() {
    const items = [
        { "ip_address":"192.168.200.101", "username":"admin", "password":"admin123", "type_device":"Router", "network_driver":"ios", "optional_args":`{ 'secret':'cisconpa55'}`, "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
        { "ip_address":"255.255.255.255", "username":"admin", "password":"admin123", "type_device":"Router", "network_driver":"junos", "created_at":"20:30:10, 25-01-2021", "updated_at": "20:30:11, 25-01-2021"},
        { "ip_address":"192.168.200.12", "username":"admin", "password":"admin123", "type_device":"Switch", "network_driver":"eos", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:12, 25-01-2021"},
        { "ip_address":"192.168.200.10", "username":"admin", "password":"admin123", "type_device":"Router", "network_driver":"ros", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
        { "ip_address":"192.168.200.11", "username":"admin", "password":"admin123", "type_device":"Router", "network_driver":"huawei_vrp", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
        { "ip_address":"192.168.200.12", "username":"admin", "password":"admin123", "type_device":"Switch", "network_driver":"ios", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
        { "ip_address":"192.168.200.10", "username":"admin", "password":"admin123", "type_device":"Router", "network_driver":"ios", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
        { "ip_address":"192.168.200.11", "username":"admin", "password":"admin123", "type_device":"Router", "network_driver":"ios", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
        { "ip_address":"192.168.200.12", "username":"admin", "password":"admin123", "type_device":"Switch", "network_driver":"ios", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
        { "ip_address":"192.168.200.10", "username":"admin", "password":"admin123", "type_device":"Router", "network_driver":"ios", "created_at":"20:30:10, 25-01-2021", "updated_at":"20:30:10, 25-01-2021"},
    ]
    return items;
}
function getDevicesInformations(){
    const items={
        "fqdn":"cisco.com",
        "hostname":"CiscoRouter",
        "interface_list":['fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3','fa0/1','fa0/2','fa0/3'],
        "model":"3625",
        "version":"3600",
        "serial_number":"fjdskf493u4oefo",
        "uptime":"1200",
        "vendor":"cisco"
    }

    return items
}

function getDeviceInterfaces() {
    const responses=[
        { "name": "FastEthernet0/1", "is_enabled": "true", "is_up": "true", "description": "", "mac_address": "ab:01:0c:02:0b:0f", "mtu": "1500", "speed": "100"},
        { "name": "FastEthernet0/2", "is_enabled": "true", "is_up": "true", "description": "", "mac_address": "ab:01:0c:02:0b:09", "mtu": "1500", "speed": "100"},
        { "name": "FastEthernet0/3", "is_enabled": "true", "is_up": "true", "description": "", "mac_address": "ab:01:0c:02:0b:08", "mtu": "1500", "speed": "100"},
        { "name": "FastEthernet0/4", "is_enabled": "true", "is_up": "true", "description": "", "mac_address": "ab:01:0c:02:0b:07", "mtu": "1500", "speed": "100"},
    ]
    return responses;
}


function getDeviceARP() {
    const responses=[
        { "interface": "FastEthernet0/1", "mac": "ab:01:0c:02:0b:0f", "ip": "192.168.10.1", "age": "1.0"},
        { "interface": "FastEthernet0/2", "mac": "ab:01:0c:02:0b:09", "ip": "192.168.100.2", "age": "1.0"},
        { "interface": "FastEthernet0/3", "mac": "ab:01:0c:02:0b:08", "ip": "192.168.20.1", "age": "1.0"},
        { "interface": "FastEthernet0/4", "mac": "ab:01:0c:02:0b:07", "ip": "192.168.200.2", "age": "1.0"},
    ]
    return responses;
}

export { getDevices, getDevicesInformations, getDeviceInterfaces, getDeviceARP }