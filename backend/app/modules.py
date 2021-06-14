from ipaddress import IPv4Network
import napalm
from napalm_ros import ros
import json
from app.serializers import DeviceRestoreSerializer
from app.models import Device
from netmiko import ConnectHandler

class Modules():

    #Check Connection----------------------------------------------------------------------------------------------------------------------
    def get_connection(ip_add):
        #PING
        import os
        response=os.system("ping -c 2 " + ip_add)
        if response==0:
            return 'Connected'
        else:
            return 'Disconnected'

    #End Check Connection-------------------------------------------------------------------------------------------------------------------
    
    #Get Device-----------------------------------------------------------------------------------------------------------------------------
    def get_device(pk):
        try:
            return Device.objects.filter(id_device=pk)
        except Device.DoesNotExist:
            return False


    #End Get Device-------------------------------------------------------------------------------------------------------------------------
    
    #Get Existing Configuration-------------------------------------------------------------------------------------------------------------
    def get_existing_configuration(device):
        driver = napalm.get_network_driver(device.network_driver)

        if device.network_driver=='ros':
            Device = {'device_type':'mikrotik_routeros','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
            result=[]

            try:
                result.append(connection.send_command('ip firewall filter export verbose'))
                result.append(connection.send_command('ipv6 firewall filter export verbose'))
                results='\n'.join(map(str, result))

                return {"rule":results,"applying":''}

            except:
                return 'Cannot connect to device'

        elif device.network_driver=='ios' or device.network_driver=='eos' :
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                int_commands=['show running-config | include interface | access-group | traffic-filter']
                int_result = device.cli(int_commands)['show running-config | include interface | access-group | traffic-filter']
                rule_commands=['show running-config | include access-list | permit | deny']
                rule_result = device.cli(rule_commands)['show running-config | include access-list | permit | deny']
                device.close()
                data_int=[]
                data_interface=[]
                int=int_result.split('\n')
                for data in int:
                    if 'interface' in data:
                        data_int.clear()
                        data_int.append(data.partition('interface')[2])
                    elif 'access-group' in data:
                        interface=data_int[0]
                        filter=data.partition('access-group')[2]
                        if 'in' in filter:
                            data_interface.append("interface"+interface+"\n ip access-group"+filter.partition('in')[0]+" in")
                        elif 'out' in filter:
                            data_interface.append("interface"+interface+"\n ip access-group"+filter.partition('out')[0]+" out")
                    elif 'traffic-filter' in data:
                        interface=data_int[0]
                        filter=data.partition('traffic-filter')[2]
                        if 'in' in filter:
                            data_interface.append({"Interface": interface, "type":"ipv6", "filterIn":filter.partition('in')[0]})
                        elif 'out' in filter:
                            data_interface.append({"Interface": interface, "type":"ipv6", "filterOut":filter.partition('out')[0]})

                return {"rule":rule_result,"applying":int_result}
            except:
                return 'Cannot connect to device'

        elif device.network_driver=='huawei_vrp':
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                commands=['display cur | include acl name|acl ipv6 name|rule|interface|traffic-filter']
                result = device.cli(commands)['display cur | include acl name|acl ipv6 name|rule|interface|traffic-filter']
                device.close()

                return {"rule":result,"applying":''}
            except:
                return 'Cannot connect to device'

        elif device.network_driver=='junos':
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                rules_commands=['show configuration | find interfaces']
                rules_result=device.cli(rules_commands)['show configuration | find interfaces']
                device.close()

                return {"rule":rules_result,"applying":''}
            except:
                return 'Cannot connect to device'

    #End Get Existing Configuration---------------------------------------------------------------------------------------------------------
    
    
    #Get Information------------------------------------------------------------------------------------------------------------------------
    def get_informations(device):
        #NAPALM get_facts()
        driver = napalm.get_network_driver(device.network_driver)

        if device.optional_args:
            optional_args=eval(device.optional_args)
            device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
        else:
            device = driver(hostname=device.ip_address, username=device.username, password=device.password)

        try:
            device.open()
            result=device.get_facts()
            if result:
                return result
            return False
        except:
            return 'Cannot connect to device'

    #End Get Information--------------------------------------------------------------------------------------------------------------------
    
    
    #Get Interface--------------------------------------------------------------------------------------------------------------------------
    def get_interfaces(device):
        #NAPALM get_interfaces()
        driver = napalm.get_network_driver(device.network_driver)

        if device.optional_args:
            optional_args=eval(device.optional_args)
            device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
        else:
            device = driver(hostname=device.ip_address, username=device.username, password=device.password)
        try:
            device.open()
            result = device.get_interfaces()
            device.close()

            if result:
                return result
            return False
        except:
            return 'Cannot connect to device'

    #End Get Interface----------------------------------------------------------------------------------------------------------------------
    
    
    #Get Table ARP--------------------------------------------------------------------------------------------------------------------------
    def get_arp_tables(device):
        #NAPALM get_arp_table()
        driver = napalm.get_network_driver(device.network_driver)

        if device.optional_args:
            optional_args=eval(device.optional_args)
            device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
        else:
            device = driver(hostname=device.ip_address, username=device.username, password=device.password)

        try:
            device.open()
            result = device.get_arp_table()
            device.close()

            if result:
                return result
            return False
        except:
            return 'Cannot connect to device'

    #End Get Table ARP----------------------------------------------------------------------------------------------------------------------
    
    
    #Run Backup-----------------------------------------------------------------------------------------------------------------------------
    def run_backup(id_device, device):
        driver = napalm.get_network_driver(device.network_driver)

        if device.network_driver=='ios' or device.network_driver=='eos' :
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)
 
            try:
                device.open()
                commands=['show running-config | include interface | access-group | traffic-filter | access-list | permit | deny']
                result = device.cli(commands)['show running-config | include interface | access-group | traffic-filter | access-list | permit | deny']
                device.close()
  
                return result
            except:
                return 'Cannot connect to device'

        elif device.network_driver=='huawei_vrp':
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)
 
            try:
                device.open()
                commands=['display cur | include acl name|acl ipv6 name|rule|interface|traffic-filter']
                result = device.cli(commands)['display cur | include acl name|acl ipv6 name|rule|interface|traffic-filter']
                device.close()
                
                return result
            except:
                return 'Cannot connect to device'

        elif device.network_driver=='junos':
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                commands=['show configuration | find interface']
                result=device.cli(commands)['show configuration | find interface']
                device.close()

                return result
            except:
                return 'Cannot connect to device'

        elif device.network_driver=='ros':
            Device = {'device_type':'mikrotik_routeros','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
            result=[]

            try:
                result.append(connection.send_command('ip firewall filter export verbose'))
                result.append(connection.send_command('ipv6 firewall filter export verbose'))
                results='\n'.join(map(str, result))

                return results
            except:
                return 'Cannot connect to device'

    #End Run Backup-------------------------------------------------------------------------------------------------------------------------
    
    
    #Run Restore----------------------------------------------------------------------------------------------------------------------------
    def run_restore(pk, file):
        config=file.read()
        restore=config.decode()

        device=Modules.get_device(pk)[0]
        driver = napalm.get_network_driver(device.network_driver)
 
        if device.network_driver=='ios' or device.network_driver=='eos':
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:                
                device.open()
                device.load_merge_candidate(config=restore)
                device.commit_config()
                device.close()

                data_result={"device":pk,"restore":restore,"status":"success"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data

            except:
                data_result={"device":pk,"restore":"Cannot connect to device","status":"failed"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data


        elif device.network_driver=='huawei_vrp':
            Device = {'device_type':'huawei','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
 
            try:
                connection.send_config_set(restore)
                data_result={"device":pk,"restore":restore,"status":"success"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data

            except:
                data_result={"device":pk,"restore":"Cannot connect to device","status":"failed"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data

        elif device.network_driver=='junos':
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:                
                device.open()
                device.load_merge_candidate(config=restore)
                device.commit_config()
                device.close()

                data_result={"device":pk,"restore":restore,"status":"success"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data

            except:
                data_result={"device":pk,"restore":"Cannot connect to device","status":"failed"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data

        elif device.network_driver=='ros':
            Device = {'device_type':'mikrotik_routeros','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
            
            try:
                connection.send_command(restore)
                data_result={"device":pk,"restore":restore,"status":"success"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data

            except:
                data_result={"device":pk,"restore":"Cannot connect to device","status":"failed"}
                serializer = DeviceRestoreSerializer(data=data_result)
                if serializer.is_valid():
                    serializer.save()
                    return serializer.data

    #End Run Restore------------------------------------------------------------------------------------------------------------------------
    
    
    #Run ACL IPv4 Configuration-------------------------------------------------------------------------------------------------------------
    def run_configuration(device, config):
        id=device.id_device
        if device.network_driver=='ios' :
            commands=Modules.get_syntax(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='eos' :
            commands=Modules.get_syntax(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='junos' :
            commands=Modules.get_syntax(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='huawei_vrp' :
            commands=Modules.get_syntax(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            Device = {'device_type':'huawei','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
 
            try:
                connection.send_config_set(cli)
                return {"device":id,"config":cli,"status":"success"}

            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='ros' :
            commands=Modules.get_syntax(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            Device = {'device_type':'mikrotik_routeros','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         

            try:
                connection.send_config_set(commands)
                return {"device":id,"config":cli,"status":"success"}

            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}
    
    #End Run ACL IPv4 Configuration---------------------------------------------------------------------------------------------------------
    
    
    #Run ACL IPv6 Configuration-------------------------------------------------------------------------------------------------------------
    def run_configuration_ipv6(device, config):
        id=device.id_device
        if device.network_driver=='ios' :
            commands=Modules.get_syntax_ipv6(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='eos' :
            commands=Modules.get_syntax_ipv6(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                print(cli)
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='junos' :
            commands=Modules.get_syntax_ipv6(device.network_driver, config)
            cli='\n'.join(map(str, commands))
            
            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='huawei_vrp' :
            commands=Modules.get_syntax_ipv6(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            Device = {'device_type':'huawei','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
 
            try:
                connection.send_config_set(cli)
                return {"device":id,"config":cli,"status":"success"}

            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='ros' :
            commands=Modules.get_syntax_ipv6(device.network_driver, config)
            cli='\n'.join(map(str, commands))

            Device = {'device_type':'mikrotik_routeros','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         

            try:
                connection.send_config_set(commands)
                return {"device":id,"config":cli,"status":"success"}

            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

    #End Run ACL IPv6 Configuration---------------------------------------------------------------------------------------------------------
    
    
    #Run ACL CLI Configuration--------------------------------------------------------------------------------------------------------------
    def run_cli_configuration(device, config):
        id=device.id_device
        cli=config['cli']

        if device.network_driver=='ios' :
            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='eos' :
            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='junos' :
            driver = napalm.get_network_driver(device.network_driver)
            if device.optional_args:
                optional_args=eval(device.optional_args)
                device = driver(hostname=device.ip_address, username=device.username, password=device.password, optional_args=optional_args)
            else:
                device = driver(hostname=device.ip_address, username=device.username, password=device.password)

            try:
                device.open()
                device.load_merge_candidate(config=cli)
                try:
                    device.commit_config()
                    #success configuration
                    return {"device":id,"config":cli,"status":"success"}
                except:
                    #failed configuration
                    return {"device":id,"config":cli,"status":"failed"}
                device.close()
            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='huawei_vrp' :
            Device = {'device_type':'huawei','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
 
            try:
                connection.send_config_set(cli)
                return {"device":id,"config":cli,"status":"success"}

            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

        elif device.network_driver=='ros' :
            Device = {'device_type':'mikrotik_routeros','ip':device.ip_address,'username':device.username,'password':device.password}
            connection = ConnectHandler(**Device)         
 
            try:
                connection.send_command(cli)
                return {"device":id,"config":cli,"status":"success"}

            except:
                #Cannot connect to device
                return {"device":id,"config":cli,"status":"failed"}

    #End Run ACL CLI Configuration----------------------------------------------------------------------------------------------------------
    
    
    #Syntax ACL IPv4 Configuration----------------------------------------------------------------------------------------------------------
    def get_syntax(vendor, config):
        rules=config['rule']
        int=config['apply'][0]['interface']
        typeTraffic=config['apply'][0]['typeTraffic']
        aclName=config['aclName']

        if vendor=='ios' :
            cli=['ip access-list extended '+aclName]

            if rules[0]['description'] :
                cli.append('remark '+rules[0]['description'])

            for rule in rules :
                src_wildcard=''
                dst_wildcard=''

                if rule['sourcePrefix']:
                    src_wildcard=IPv4Network(rule['source']+'/'+str(rule['sourcePrefix'])).hostmask
                    src_wildcard=str(src_wildcard)
                
                if rule['destinationPrefix']:
                    dst_wildcard=IPv4Network(rule['destination']+'/'+str(rule['destinationPrefix'])).hostmask
                    dst_wildcard=str(dst_wildcard)
                
                if src_wildcard and dst_wildcard and rule['sourcePort'] and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' eq '+rule['sourcePort']+' '+rule['destination']+' '+dst_wildcard+' eq '+rule['destinationPort'])

                elif src_wildcard and dst_wildcard and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' '+rule['destination']+' '+dst_wildcard+' eq '+rule['destinationPort'])

                elif src_wildcard and dst_wildcard and rule['sourcePort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' eq '+rule['sourcePort']+' '+rule['destination']+' '+dst_wildcard)

                elif src_wildcard and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' host '+rule['destination']+' eq '+rule['destinationPort'])

                elif dst_wildcard and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+' '+dst_wildcard+' eq '+rule['destinationPort'])
                
                elif src_wildcard and dst_wildcard:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' '+rule['destination']+' '+dst_wildcard)
                
                elif src_wildcard:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' host '+rule['destination'])

                elif dst_wildcard:
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+' '+dst_wildcard)

                elif rule['source']=='any' and rule['destination']=='any' :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+rule['destination'])

            cli.append('interface '+int)
            cli.append('ip access-group '+aclName+' '+typeTraffic)
            return cli

        elif vendor=='eos' :
            cli=['ip access-list '+aclName]

            if rules[0]['description'] :
                cli.append('remark '+rules[0]['description'])

            for rule in rules :
                src_wildcard=''
                dst_wildcard=''

                if rule['sourcePrefix']:
                    src_wildcard=IPv4Network(rule['source']+'/'+str(rule['sourcePrefix'])).hostmask
                    src_wildcard=str(src_wildcard)
                
                if rule['destinationPrefix']:
                    dst_wildcard=IPv4Network(rule['destination']+'/'+str(rule['destinationPrefix'])).hostmask
                    dst_wildcard=str(dst_wildcard)

                
                if src_wildcard and dst_wildcard and rule['sourcePort'] and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' eq '+rule['sourcePort']+' '+rule['destination']+' '+dst_wildcard+' eq '+rule['destinationPort'])

                elif src_wildcard and dst_wildcard and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' '+rule['destination']+' '+dst_wildcard+' eq '+rule['destinationPort'])

                elif src_wildcard and dst_wildcard and rule['sourcePort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' eq '+rule['sourcePort']+' '+rule['destination']+' '+dst_wildcard)

                elif src_wildcard and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' host '+rule['destination']+' eq '+rule['destinationPort'])

                elif dst_wildcard and rule['destinationPort']:
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+' '+dst_wildcard+' eq '+rule['destinationPort'])
                
                elif src_wildcard and dst_wildcard:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' '+rule['destination']+' '+dst_wildcard)
                
                elif src_wildcard:
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+src_wildcard+' host '+rule['destination'])

                elif dst_wildcard:
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+' '+dst_wildcard)

                elif rule['source']=='any' and rule['destination']=='any' :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+rule['destination'])

            #cli.append('control-panel')
            #cli.append('ip access-group '+aclName+' '+typeTraffic)
            return cli

        elif vendor=='junos' :
            cli=['edit firewall family inet filter '+aclName]
            
            if rules[0]['description'] :
                cli.append('annotate term '+aclName+' '+rules[0]['description'])
       
            traffic=''
            if typeTraffic=='in' :
                traffic="input"

            elif typeTraffic=='out':
                traffic='output'

            for rule in rules :
                action=''
                source=rule['source']
                destination=rule['destination']

                if rule['action']=='permit' :
                    action="accept"

                elif rule['action']=='deny':
                    action='discard'

                if rule['sourcePrefix']:
                    source=source+'/'+rule['sourcePrefix']

                if rule['destinationPrefix']:
                    destination=destination+'/'+rule['destinationPrefix']
                
                if source and destination and rule['sourcePort'] and rule['destinationPort']:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' from source-port '+rule['sourcePort'])
                    cli.append('set term '+aclName+' from destination-port '+rule['destinationPort'])
                    cli.append('set term '+aclName+' then '+action)

                elif source and destination and rule['destinationPort']:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' from destination-port '+rule['destinationPort'])
                    cli.append('set term '+aclName+' then '+action)

                elif source and destination and rule['sourcePort']:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' from source-port '+rule['sourcePort'])
                    cli.append('set term '+aclName+' then '+action)

                elif source and destination:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' then '+action)

                else:
                    cli.append('set term term-default then '+action)

            cli.append('top')
            cli.append('set interfaces '+int+' unit 0 family inet filter '+traffic+' '+aclName)

            return cli

        elif vendor=='huawei_vrp' :
            cli=['acl name '+aclName]
            if rules[0]['description'] :
                cli.append('description '+rules[0]['description'])

            for rule in rules :
                src_wildcard=''
                dst_wildcard=''

                if rule['sourcePrefix']:
                    src_wildcard=IPv4Network(rule['source']+'/'+str(rule['sourcePrefix'])).hostmask
                    src_wildcard=str(src_wildcard)
                
                if rule['destinationPrefix']:
                    dst_wildcard=IPv4Network(rule['destination']+'/'+str(rule['destinationPrefix'])).hostmask
                    dst_wildcard=str(dst_wildcard)

                if src_wildcard and dst_wildcard and rule['sourcePort'] and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' '+src_wildcard+' source-port eq '+rule['sourcePort']+' destination '+rule['destination']+' '+dst_wildcard+' destination-port eq '+rule['destinationPort'])

                elif src_wildcard and dst_wildcard and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' '+src_wildcard+' destination '+rule['destination']+' '+dst_wildcard+' destination-port eq '+rule['destinationPort'])

                elif src_wildcard and dst_wildcard and rule['sourcePort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' '+src_wildcard+' source-port eq '+rule['sourcePort']+' destination '+rule['destination']+' '+dst_wildcard)

                elif src_wildcard and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' '+src_wildcard+' destination '+rule['destination']+' 0 destination-port eq '+rule['destinationPort'])

                elif dst_wildcard and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' 0 destination '+rule['destination']+' '+dst_wildcard+' destination-port eq '+rule['destinationPort'])

                elif src_wildcard and dst_wildcard:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' '+src_wildcard+' destination '+rule['destination']+' '+dst_wildcard)

                elif src_wildcard:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' '+src_wildcard+' destination '+rule['destination']+' 0')

                elif dst_wildcard:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' 0 destination '+rule['destination']+' '+dst_wildcard)

                elif rule['source']=='any' and rule['destination']=='any' :
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' destination '+rule['destination'])

            cli.append('interface '+int)
            cli.append('traffic-filter '+typeTraffic+' acl name '+aclName)
            return cli

        elif vendor=='ros' :
            cli=['/ip firewall filter']
  
            for rule in rules:
                action=''
                if rule['action']=='permit' :
                    action='accept'
                elif rule['action']:
                    action='discard'

                if rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])                    


                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' out-interface='+int+' comment='+rule['description'])

                
                elif rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and rule['destinationPrefix'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' out-interface='+int+' comment='+rule['description'])


                elif rule['destinationPrefix'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['destinationPrefix'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' out-interface='+int+' comment='+rule['description'])


                elif rule['source'] and rule['destination'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['source'] and rule['destination'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+' out-interface='+int+' comment='+rule['description'])

            return cli

    #End Syntax ACL IPv4 Configuration------------------------------------------------------------------------------------------------------
    
    
    #Syntax ACL IPv6 Configuration----------------------------------------------------------------------------------------------------------
    def get_syntax_ipv6(vendor, config):
        rules=config['rule']
        int=config['apply'][0]['interface']
        typeTraffic=config['apply'][0]['typeTraffic']
        aclName=config['aclName']

        if vendor=='ios' :
            cli=['ipv6 access-list '+aclName]

            if rules[0]['description'] :
                cli.append('remark '+rules[0]['description'])

            for rule in rules :
                if rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and rule['destinationPort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' eq '+rule['sourcePort']+' '+rule['destination']+'/'+rule['destinationPrefix']+' eq '+rule['destinationPort'])

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['destinationPort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' '+rule['destination']+'/'+rule['destinationPrefix']+' eq '+rule['destinationPort'])

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' eq '+rule['sourcePort']+' '+rule['destination']+'/'+rule['destinationPrefix'])

                elif rule['sourcePrefix'] and rule['destinationPort'] :
                     cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' host '+rule['destination']+' eq '+rule['destinationPort'])

                elif rule['destinationPrefix'] and rule['destinationPort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+'/'+rule['destinationPrefix']+' eq '+rule['destinationPort'])
                
                elif rule['sourcePrefix'] and rule['destinationPrefix'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' '+rule['destination']+'/'+rule['destinationPrefix'])
                
                elif rule['sourcePrefix'] :
                     cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' host '+rule['destination'])

                elif rule['destinationPrefix'] :
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+'/'+rule['destinationPrefix'])

                elif rule['source']=='any' and rule['destination']=='any' :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+rule['destination'])
            
            cli.append('interface '+int)
            cli.append('ipv6 traffic-filter '+aclName+' '+typeTraffic)
            return cli

        elif vendor=='eos' :
            cli=['ipv6 access-list '+aclName]

            if rules[0]['description'] :
                cli.append('remark '+rules[0]['description'])

            for rule in rules :
                if rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and rule['destinationPort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' eq '+rule['sourcePort']+' '+rule['destination']+'/'+rule['destinationPrefix']+' eq '+rule['destinationPort'])

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['destinationPort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' '+rule['destination']+'/'+rule['destinationPrefix']+' eq '+rule['destinationPort'])

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' eq '+rule['sourcePort']+' '+rule['destination']+'/'+rule['destinationPrefix'])

                elif rule['sourcePrefix'] and rule['destinationPort'] :
                     cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' host '+rule['destination']+' eq '+rule['destinationPort'])

                elif rule['destinationPrefix'] and rule['destinationPort'] :
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+'/'+rule['destinationPrefix']+' eq '+rule['destinationPort'])
                
                elif rule['sourcePrefix'] and rule['destinationPrefix'] :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' '+rule['destination']+'/'+rule['destinationPrefix'])
                
                elif rule['sourcePrefix'] :
                     cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+'/'+rule['sourcePrefix']+' host '+rule['destination'])

                elif rule['destinationPrefix'] :
                    cli.append(rule['action']+' '+rule['protocol']+' host '+rule['source']+' '+rule['destination']+'/'+rule['destinationPrefix'])

                elif rule['source']=='any' and rule['destination']=='any' :
                    cli.append(rule['action']+' '+rule['protocol']+' '+rule['source']+' '+rule['destination'])

            #cli.append('control-panel')
            #cli.append('ipv6 access-group '+aclName+' '+typeTraffic)
            return cli

        elif vendor=='junos' :
            cli=['edit firewall family inet6 filter '+aclName]
            if rules[0]['description'] :
                cli.append('annotate term '+aclName+' '+rules[0]['description'])

            traffic=''
            if typeTraffic=='in' :
                traffic="input"

            elif typeTraffic=='out':
                traffic='output'
            
            for rule in rules :
                action=''
                source=rule['source']
                destination=rule['destination']

                if rule['action']=='permit' :
                    action="accept"

                elif rule['action']=='deny':
                    action='discard'

                if rule['sourcePrefix']:
                    source=source+'/'+rule['sourcePrefix']

                if rule['destinationPrefix']:
                    destination=destination+'/'+rule['destinationPrefix']

                if source and destination and rule['sourcePort'] and rule['destinationPort']:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from payload-protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' from source-port '+rule['sourcePort'])
                    cli.append('set term '+aclName+' from destination-port '+rule['destinationPort'])
                    cli.append('set term '+aclName+' then '+action)

                elif source and destination and rule['destinationPort']:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from payload-protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' from destination-port '+rule['destinationPort'])
                    cli.append('set term '+aclName+' then '+action)

                elif source and destination and rule['sourcePort']:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from payload-protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' from source-port '+rule['sourcePort'])
                    cli.append('set term '+aclName+' then '+action)

                elif source and destination:
                    cli.append('set term '+aclName+' from source-address '+source)
                    cli.append('set term '+aclName+' from destination-address '+destination)
                    cli.append('set term '+aclName+' from payload-protocol '+rule['protocol'])
                    cli.append('set term '+aclName+' then '+action)

                else :
                    cli.append('set term term-default then '+action)

            cli.append('top')
            cli.append('set interfaces '+int+' unit 0 family inet6 filter '+traffic+' '+aclName)

            return cli

        elif vendor=='huawei_vrp' :
            cli=['acl ipv6 name '+aclName]

            if rules[0]['description'] :
                cli.append('description '+rules[0]['description'])

            for rule in rules :
                if rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+'/'+ rule['sourcePrefix']+' source-port eq '+rule['sourcePort']+' destination '+rule['destination']+'/'+rule['destinationPrefix']+' destination-port eq '+rule['destinationPort'])

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+'/'+ rule['sourcePrefix']+' destination '+rule['destination']+'/'+rule['destinationPrefix']+' destination-port eq '+rule['destinationPort'])

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+'/'+ rule['sourcePrefix']+' source-port eq '+rule['sourcePort']+' destination '+rule['destination']+'/'+rule['destinationPrefix'])

                elif rule['sourcePrefix'] and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+'/'+ rule['sourcePrefix']+' destination '+rule['destination']+' destination-port eq '+rule['destinationPort'])

                elif rule['destinationPrefix'] and rule['destinationPort']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' destination '+rule['destination']+'/'+rule['destinationPrefix']+' destination-port eq '+rule['destinationPort'])

                elif rule['sourcePrefix'] and rule['destinationPrefix']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+'/'+ rule['sourcePrefix']+' destination '+rule['destination']+'/'+rule['destinationPrefix'])

                elif rule['sourcePrefix']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+'/'+ rule['sourcePrefix']+' destination '+rule['destination'])

                elif rule['destinationPrefix']:
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' destination '+rule['destination']+'/'+rule['destinationPrefix'])

                elif rule['source']=='any' and rule['destination']=='any' :
                    cli.append('rule '+rule['action']+' '+rule['protocol']+' source '+rule['source']+' destination '+rule['destination'])
            
            cli.append('interface '+int)
            cli.append('traffic-filter '+typeTraffic+' acl name '+aclName)
            return cli

        elif vendor=='ros' :
            cli=['/ipv6 firewall filter']
  
            for rule in rules:
                action=''
                if rule['action']=='permit' :
                    action='accept'
                elif rule['action']:
                    action='discard'

                if rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])                        


                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and rule['sourcePort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' src-port='+rule['sourcePort']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' out-interface='+int+' comment='+rule['description'])

                
                elif rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['destinationPrefix'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and rule['destinationPort'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' dst-port='+rule['destinationPort']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPort'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' dst-port='+rule['destinationPort']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and rule['destinationPrefix'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and rule['destinationPrefix'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' out-interface='+int+' comment='+rule['description'])


                elif rule['destinationPrefix'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['destinationPrefix'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+'/'+rule['destinationPrefix']+' out-interface='+int+' comment='+rule['description'])


                elif rule['sourcePrefix'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['sourcePrefix'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+'/'+rule['sourcePrefix']+' dst-address='+rule['destination']+' out-interface='+int+' comment='+rule['description'])


                elif rule['source'] and rule['destination'] and typeTraffic=='in':
                    cli.append('add chain=input action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+' in-interface='+int+' comment='+rule['description'])                        

                elif rule['source'] and rule['destination'] and typeTraffic=='out':
                    cli.append('add chain=output action='+action+' protocol='+rule['protocol']+' src-address='+rule['source']+' dst-address='+rule['destination']+' out-interface='+int+' comment='+rule['description'])

            return cli

     #End Syntax ACL IPv6 Configuration------------------------------------------------------------------------------------------------------
