function postDevice(device){
    const responses=
    {
        "fqdn":"cisco.com",
        "hostname":"CiscoRouter",
        "interface_list":"['fa0/0','fa0/1']",
        "model":"3625",
        "os_version":"3600",
        "serial_number":"dfhajfe374rfesfsd",
        "uptime":"1200",
        "vendor":"cisco"
      }

    if(device.ip_address){
        return responses
    }
    else{
        return 'not found'
    }
}


export { postDevice }