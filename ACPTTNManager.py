import json
import requests

# Class used to define a TTN Application client.
class Client:
    url = ''
    headers = ''

    def __init__(self, version, url, headers):
        self.version = version
        self.url = url
        self.headers = headers


class ACPTTNManager:

    client = ''

    def __init__(self, settings, app_id):
        self.settings = settings
        version = self.settings['TTN_APPLICATIONS'][app_id]['version']
        self.client = Client(
                        version,
                        self.settings['URLS'][str(version)]['url'] + self.settings['TTN_APPLICATIONS'][app_id]['app_id'],
                        {"Authorization": self.settings['TTN_APPLICATIONS'][app_id]['auth_type'] + " "+ self.settings['TTN_APPLICATIONS'][app_id]['access_key'], "Content-Type":"application/json"})

    def get_app_details(self):
        '''
        Return the TTN Application object
        '''
        response = requests.get(self.client.url,headers=self.client.headers)
        return response.json()

    def get_all_devices(self, client=None):
        '''
        Return all devices registered on the specified client application
        client: The application client. Use the default application client if None
        '''
        if client == None:
            client = self.client
        
        if client.version == 2:
            response = requests.get(client.url+"/devices",headers=client.headers)
            return response.json()
        
        tmp_split = client.url.split('/')
        js_url = '/'.join(tmp_split[:-2])+'/js/'+'/'.join(tmp_split[-2:])
        ns_url = '/'.join(tmp_split[:-2])+'/ns/'+'/'.join(tmp_split[-2:])

        field_mask_is = ','.join(self.settings['ID_SERVER_MASKS']['paths'])
        field_mask_js = ','.join(self.settings['JOIN_SERVER_MASKS']['paths'])
        field_mask_ns = ','.join(self.settings['NETWORK_SERVER_MASKS']['paths'])

        response_is = requests.get(client.url+"/devices?field_mask="+field_mask_is,headers=client.headers)

        end_devices = {'end_devices':[]}

        for device in response_is.json()['end_devices']:
            device_id = device['ids']['device_id']
            response_js = requests.get(js_url+"/devices/"+device_id+"?field_mask="+field_mask_js,headers=client.headers)
            response_ns = requests.get(ns_url+"/devices/"+device_id+"?field_mask="+field_mask_ns,headers=client.headers)
            
            js_dict = response_js.json()
            ns_dict = response_ns.json()

            for key in js_dict.keys():
                device[key] = js_dict[key]
            
            for key in ns_dict.keys():
                device[key] = ns_dict[key]

            end_devices['end_devices'].append(device)

        return end_devices
        

    def get_device_details(self, device_id, client=None):
        '''
        Return the device object corresponding to 'device_id' on the specified client application
        client: The application client. Use the default application client if None
        '''
        if client == None:
            client = self.client

        if client.version == 2:
            response = requests.get(client.url+"/devices/"+device_id,headers=client.headers)
            return response.json()

        tmp_split = client.url.split('/')
        js_url = '/'.join(tmp_split[:-2])+'/js/'+'/'.join(tmp_split[-2:])
        ns_url = '/'.join(tmp_split[:-2])+'/ns/'+'/'.join(tmp_split[-2:])

        field_mask_is = ','.join(self.settings['ID_SERVER_MASKS']['paths'])
        field_mask_js = ','.join(self.settings['JOIN_SERVER_MASKS']['paths'])
        field_mask_ns = ','.join(self.settings['NETWORK_SERVER_MASKS']['paths'])

        response_is = requests.get(client.url+"/devices/"+device_id+"?field_mask="+field_mask_is,headers=client.headers)

        response_js = requests.get(js_url+"/devices/"+device_id+"?field_mask="+field_mask_js,headers=client.headers)
        response_ns = requests.get(ns_url+"/devices/"+device_id+"?field_mask="+field_mask_ns,headers=client.headers)
        
        device = response_is.json()
        js_dict = response_js.json()
        ns_dict = response_ns.json()

        for key in js_dict.keys():
            device[key] = js_dict[key]
        
        for key in ns_dict.keys():
            device[key] = ns_dict[key]
        
        return device
        


    def register_device(self, device_settings, migration=False):
        '''
        Register a device with the details provided in device_settings
        '''
        response_text = ''
        if self.client.version == 2:
            device = None
            if not migration:
                device = self.get_device_v2(device_settings)
            else:
                device = device_settings
            response = requests.post(self.client.url+"/devices",headers=self.client.headers, data=json.dumps(device))
            if response.status_code == 200:
                return 'Device added'
            else:
                return response.json()

        device = None
        if not migration:
            device = self.get_device(device_settings)            
        else:
            device = device_settings
        
        device_id = device['is']['end_device']['ids']['device_id']
        tmp_split = self.client.url.split('/')

        ### Register on End Device registry
        isUpdate = False
        response_is = requests.post(self.client.url+"/devices", headers=self.client.headers, data=json.dumps(device['is']))
        if response_is.status_code == 409:
            response_is = requests.put(self.client.url+"/devices/"+device_id, headers=self.client.headers, data=json.dumps(device['is']))
            isUpdate = True
        response_js, response_ns, response_as = '', '', ''
        response_text = response_is.text
        
        ### Register on Join Server registry
        if response_is.status_code == 200:
            js_url = '/'.join(tmp_split[:-2])+'/js/'+'/'.join(tmp_split[-2:])+"/devices/"+device_id
            response_js = requests.put(js_url, headers=self.client.headers, data=json.dumps(device['js']))
            if response_js.status_code == 200 and isUpdate:
                return 'Device updated'
            response_text += response_js.text
        else:
            return response_text
        
        ### Register on Network Server registry
        if response_js.status_code == 200:
            ns_url = '/'.join(tmp_split[:-2])+'/ns/'+'/'.join(tmp_split[-2:])+"/devices/"+device_id
            response_ns = requests.put(ns_url, headers=self.client.headers, data=json.dumps(device['ns']))
            response_text += response_ns.text
        else:
            response = requests.delete(self.client.url+"/devices/"+device_id, headers=self.client.headers)
            return response_text + response.text
        
        ### Register on Application Server registry
        if response_ns.status_code == 200:            
            as_url = '/'.join(tmp_split[:-2])+'/as/'+'/'.join(tmp_split[-2:])+"/devices/"+device_id
            response_as = requests.put(as_url, headers=self.client.headers, data=json.dumps(device['as']))
            response_text += response_as.text
        else:
            js_url = '/'.join(tmp_split[:-2])+'/js/'+'/'.join(tmp_split[-2:])+"/devices/"+device_id
            response = requests.delete(js_url, headers=self.client.headers)
            response_text += response.text
            
            response = requests.delete(self.client.url+"/devices/"+device_id, headers=self.client.headers)
            return response_text + response.text
        
        if response_as.status_code != 200:
            ns_url = '/'.join(tmp_split[:-2])+'/ns/'+'/'.join(tmp_split[-2:])+"/devices/"+device_id
            response = requests.delete(ns_url, headers=self.client.headers)
            response_text += response.text

            js_url = '/'.join(tmp_split[:-2])+'/js/'+'/'.join(tmp_split[-2:])+"/devices/"+device_id
            response = requests.delete(js_url, headers=self.client.headers)
            response_text += response.text
            
            response = requests.delete(self.client.url+"/devices/"+device_id, headers=self.client.headers)
            return response_text + response.text
        else:
            return 'Device added'

    def delete_device(self, dev_id, client=None):
        '''
        Delete a device with device id as dev_id.
        dev_id: Device id of the device to be deleted
        client: The TTN application client from which the devices should be removed. Use the default application client if None
        '''
        if client == None:
            client = self.client
        if client.version == 2:
            response = requests.delete(client.url+"/devices/"+dev_id, headers=client.headers)
            return response.json()
        else:
            tmp_split = client.url.split('/')
            
            try:
                as_url = '/'.join(tmp_split[:-2])+'/as/'+'/'.join(tmp_split[-2:])+"/devices/"+dev_id
                response = requests.delete(as_url, headers=self.client.headers)
            except:
                pass
            
            try:
                ns_url = '/'.join(tmp_split[:-2])+'/ns/'+'/'.join(tmp_split[-2:])+"/devices/"+dev_id
                response = requests.delete(ns_url, headers=self.client.headers)
            except:
                pass

            try:
                js_url = '/'.join(tmp_split[:-2])+'/js/'+'/'.join(tmp_split[-2:])+"/devices/"+dev_id
                response = requests.delete(js_url, headers=self.client.headers)
            except:
                pass
            
            response = requests.delete(client.url+"/devices/"+dev_id, headers=self.client.headers)

            return response.json()


    def get_device_v2(self, device_settings, app_id = None):
        if app_id == None:
            app_id = device_settings['app_id']
        device = {
                    "altitude": device_settings['altitude'] if 'altitude' in device_settings.keys() else 0,
                    "app_id": app_id,
                    "attributes": device_settings['attributes'] if 'attributes' in device_settings.keys() else {"key": "","value": ""},
                    "description": device_settings['description'] if 'description' in device_settings.keys() else "",
                    "dev_id": device_settings['dev_id'],
                    "latitude": device_settings['latitude'] if 'latitude' in device_settings.keys() else 0.0,
                    "longitude": device_settings['longitude'] if 'longitude' in device_settings.keys() else 0.0,
                    "lorawan_device": {
                        "activation_constraints": device_settings['lorawan_device']['activation_constraints'] if 'activation_constraints' in device_settings.keys() else "local",
                        "app_eui": device_settings['lorawan_device']['app_eui'],
                        "app_id": app_id,
                        "app_key": device_settings['lorawan_device']['app_key'],
                        "dev_eui": device_settings['lorawan_device']['dev_eui'],
                        "dev_id": device_settings['dev_id'],
                        "disable_f_cnt_check": False,
                        "f_cnt_down": device_settings['f_cnt_down'] if 'f_cnt_down' in device_settings.keys() else 0,
                        "f_cnt_up": device_settings['f_cnt_up'] if 'f_cnt_up' in device_settings.keys() else 0,
                        "last_seen": device_settings['last_seen'] if 'last_seen' in device_settings.keys() else 0,
                        "uses32_bit_f_cnt": True
                    }
                }
        # response = requests.post(self.client.url+"/devices",headers=self.client.headers, data=json.dumps(device))
        return device

    def get_device(self, device_settings):
        device = {}
        version = device_settings['ttn_version']
        device['is'] = {
            "end_device": {
                "ids": {
                    "device_id": device_settings['ids']['device_id'] if version == 3 else device_settings['dev_id'],
                    "dev_eui": device_settings['ids']['dev_eui']  if version == 3 else device_settings['lorawan_device']['dev_eui'],
                    "join_eui": (device_settings['ids']['join_eui'] if 'join_eui' in device_settings['ids'].keys() else self.settings['template-v3']['ids']['join_eui'])  if version == 3 else device_settings['lorawan_device']['app_eui']
                },
                "join_server_address": self.settings['template-v3']['join_server_address'],
                "network_server_address": self.settings['template-v3']['network_server_address'],
                "application_server_address": self.settings['template-v3']['application_server_address'],
                "name": device_settings['name'] if version == 3 else device_settings['dev_id'],
                "description": device_settings['description'] if 'description' in device_settings.keys() else ""
            },
            "field_mask":{
                "paths":[
                    "join_server_address",
                    "network_server_address",
                    "application_server_address",
                    "ids.dev_eui",
                    "ids.join_eui",
                    "name"
                ]
            }
        }

        device['js'] = {
            "end_device": {
                "ids": {
                    "device_id": device_settings['ids']['device_id'] if version == 3 else device_settings['dev_id'],
                    "dev_eui": device_settings['ids']['dev_eui']  if version == 3 else device_settings['lorawan_device']['dev_eui'],
                    "join_eui": (device_settings['ids']['join_eui'] if 'join_eui' in device_settings['ids'].keys() else self.settings['template-v3']['ids']['join_eui'])  if version == 3 else device_settings['lorawan_device']['app_eui']
                },
                "network_server_address": self.settings['template-v3']['join_server_address'],
                "application_server_address": self.settings['template-v3']['application_server_address'],
                "network_server_kek_label": device_settings['network_server_kek_label'] if 'network_server_kek_label' in device_settings.keys() else "",
                "application_server_kek_label": device_settings['application_server_kek_label'] if 'application_server_kek_label' in device_settings.keys() else "",
                "application_server_id": device_settings['application_server_id'] if 'application_server_id' in device_settings.keys() else "",
                "net_id":device_settings['net_id'] if 'net_id' in device_settings.keys() else None,
                "root_keys": device_settings['root_keys'] if version == 3 else {"app_key":{"key":device_settings['lorawan_device']['app_key']}}
            },
            "field_mask":{
                "paths":[
                    "network_server_address",
                    "application_server_address",
                    "ids.device_id",
                    "ids.dev_eui",
                    "ids.join_eui",
                    "network_server_kek_label",
                    "application_server_kek_label",
                    "application_server_id",
                    "net_id",
                    "root_keys.app_key.key"
                ]
            }
        }

        device['ns'] = {
            "end_device": {
                "frequency_plan_id": device_settings['frequency_plan_id'] if 'frequency_plan_id' in device_settings.keys() else self.settings['template-v3']['frequency_plan_id'],
                "supports_join": device_settings['supports_join'] if 'supports_join' in device_settings.keys() else True,
                "lorawan_version": device_settings['lorawan_version'] if 'lorawan_version' in device_settings.keys() else self.settings['template-v3']['lorawan_version'],                
                "lorawan_phy_version": device_settings['lorawan_phy_version'] if 'lorawan_phy_version' in device_settings.keys() else self.settings['template-v3']['lorawan_phy_version'],
                "ids": {
                    "device_id": device_settings['ids']['device_id'] if version == 3 else device_settings['dev_id'],
                    "dev_eui": device_settings['ids']['dev_eui']  if version == 3 else device_settings['lorawan_device']['dev_eui'],
                    "join_eui": (device_settings['ids']['join_eui'] if 'join_eui' in device_settings['ids'].keys() else self.settings['template-v3']['ids']['join_eui'])  if version == 3 else device_settings['lorawan_device']['app_eui']
                },
                "mac_settings": device_settings['mac_settings'] if 'mac_settings' in device_settings.keys() else self.settings['template-v3']['mac_settings'],
                "supports_class_c": device_settings['supports_class_c'] if 'supports_class_c' in device_settings.keys() else False,
                "supports_class_b": device_settings['supports_class_b'] if 'supports_class_b' in device_settings.keys() else False,
                "multicast": device_settings['multicast'] if 'multicast' in device_settings.keys() else False             
            },
            "field_mask":{
                "paths":[
                    "multicast",
                    "supports_join",
                    "lorawan_version",
                    "ids.device_id",
                    "ids.dev_eui",
                    "ids.join_eui",
                    "mac_settings.supports_32_bit_f_cnt",
                    "supports_class_c",
                    "supports_class_b",
                    "lorawan_phy_version",
                    "frequency_plan_id"
                ]
            }
        }

        device['as'] = {
            "end_device":{
                "ids": {
                    "device_id": device_settings['ids']['device_id'] if version == 3 else device_settings['dev_id'],
                    "dev_eui": device_settings['ids']['dev_eui']  if version == 3 else device_settings['lorawan_device']['dev_eui'],
                    "join_eui": (device_settings['ids']['join_eui'] if 'join_eui' in device_settings['ids'].keys() else self.settings['template-v3']['ids']['join_eui'])  if version == 3 else device_settings['lorawan_device']['app_eui']
                }
            },
            "field_mask":{
                "paths":[
                    "ids.device_id",
                    "ids.dev_eui",
                    "ids.join_eui"
                ]
            }
        }

        return device
        
    def migrate_devices(self, from_app_id, dev_ids = None):
        '''
        Migrate a set of devices from a TTN application with the id "from_app_id" to the default application of the class
        dev_ids: List containing the dev_id of all the devices to be migrated. Migrate all devices if None
        '''
        from_app_version = self.settings['TTN_APPLICATIONS'][from_app_id]['version']
        device_key = 'devices' if from_app_version == 2 else 'end_devices'

        migrate_client = Client(
                        from_app_version,
                        self.settings['URLS'][str(from_app_version)]['url'] + self.settings['TTN_APPLICATIONS'][from_app_id]['app_id'],
                        {"Authorization": self.settings['TTN_APPLICATIONS'][from_app_id]['auth_type'] + " "+ self.settings['TTN_APPLICATIONS'][from_app_id]['access_key'], "Content-Type":"application/json"})

        to_app = self.get_app_details()
        to_app_id = to_app['app_id'] if self.client.version == 2 else to_app['ids']['application_id']
        response_list = []
        if dev_ids == None:            
            devices = self.get_all_devices(migrate_client)

            if len(devices) == 0:
                return "No registered devices to migrate"

            for device in devices[device_key]:
                response = self.__migrate_device(device, migrate_client, to_app_id)

                if response != 'Device added':
                    response_list.append(response)
        else:
            for dev_id in dev_ids:
                device = self.get_device_details(dev_id, migrate_client)

                if 'error' in device.keys():
                    print(dev_id, ' not registered on ', from_app_id)
                    continue

                response = self.__migrate_device(device, migrate_client, to_app_id)

                if response != 'Device added':
                    response_list.append(response)

        if len(response_list) == 0:
            return "Migration complete"
        else:
            return json.dumps(response_list)    

    def __migrate_device(self, device, migrate_client, to_app_id):
        dev_id = device['dev_id'] if migrate_client.version == 2 else device['ids']['device_id']
        device["ttn_version"] = migrate_client.version
        new_device = self.get_device(device) if self.client.version == 3 else self.get_device_v2(device, to_app_id)
        new_device['ttn_version'] = self.client.version
        self.delete_device(dev_id,migrate_client)

        response = self.register_device(new_device, True)
        
        return response