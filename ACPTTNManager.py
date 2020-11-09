import json
import requests

# Class used to define a TTN Application client.
class Client:
    url = ''
    headers = ''

    def __init__(self, url, headers):
        self.url = url
        self.headers = headers


class ACPTTNManager:

    client = ''

    def __init__(self, settings, app_id):
        self.settings = settings

        self.client = Client(
                        self.settings['URL'] + self.settings['TTN_APPLICATIONS'][app_id]['app_id'],
                        {"Authorization": "Key "+self.settings['TTN_APPLICATIONS'][app_id]['access_key'], "Content-Type":"application/json"}
                )

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
        response = requests.get(client.url+"/devices",headers=client.headers)

        return response.json()
        

    def get_device_details(self, device_id, client=None):
        '''
        Return the device object corresponding to 'device_id' on the specified client application
        client: The application client. Use the default application client if None
        '''
        if client == None:
            client = self.client
        response = requests.get(client.url+"/devices/"+device_id,headers=client.headers)

        return response.json()

    def register_devices(self, devices):
        '''
        Register all devices contained in the list 'devices'
        devices: A list of device dictionaries of the form defined at https://www.thethingsnetwork.org/docs/applications/manager/api.html
        '''
        response_list = []
        for device in devices:
            response = requests.post(self.client.url+"/devices",headers=self.client.headers, data=json.dumps(device))
            if response.status_code != 200:
                response_list.append(device['dev_id']+':'+response.text)
        if len(response_list) == 0:
            return 'Device added'
        else:
            return json.dumps(response_list)
        

    def delete_device(self, dev_id, client=None):
        '''
        Delete a device with device id as dev_id.
        dev_id: Device id of the device to be deleted
        client: The TTN application client from which the devices should be removed. Use the default application client if None
        '''
        if client == None:
            client = self.client

        response = requests.delete(client.url+"/devices/"+dev_id, headers=client.headers)

        return response.json()
    
    
    def migrate_devices(self, from_app_id, dev_ids=None):
        '''
        Migrate a set of devices from a TTN application to the default application of the class
        dev_ids: List containing the dev_id of all the devices to be migrated. Migrate all devices if empty
        '''
        migrate_client = Client(
                                    url= self.settings['URL'] + self.settings['TTN_APPLICATIONS'][from_app_id]['app_id'],
                                    headers={"Authorization": "Key "+self.settings['TTN_APPLICATIONS'][from_app_id]['access_key'], "Content-Type":"application/json"}
                            )
        response_list = []
        to_app_id = self.get_app_details()['app_id']
        if dev_ids == None:            
            devices = self.get_all_devices(migrate_client)

            if len(devices) == 0:
                return "No registered devices to migrate"

            for device in devices['devices']:
                response = ACPTTNManager.__migrate_device(device, self, migrate_client, to_app_id)

                if response != 'Device added':
                    response_list.append(response)
        else:
            for dev_id in dev_ids:
                device = self.get_device_details(dev_id, migrate_client)

                if 'error' in device.keys():
                    print(dev_id, ' not registered on ', from_app_id)
                    continue

                response = ACPTTNManager.__migrate_device(device, self, migrate_client, to_app_id)

                if response != 'Device added':
                    response_list.append(response)

        if len(response_list) == 0:
            return "Migration complete"
        else:
            return json.dumps(response_list)

    #Create a device dictionary
    def get_new_device(self, device, to_app_id):
        migrate_device = {
                            "altitude": device['altitude'] if 'altitude' in device.keys() else 0,
                            "app_id": self.settings['TTN_APPLICATIONS'][to_app_id]['app_id'],
                            "attributes": device['attributes'] if 'attributes' in device.keys() else {"key": "","value": ""},
                            "description": device['description'] if 'description' in device.keys() else "",
                            "dev_id": device['dev_id'],
                            "latitude": device['latitude'] if 'latitude' in device.keys() else 0.0,
                            "longitude": device['longitude'] if 'longitude' in device.keys() else 0.0,
                            "lorawan_device": {
                                "activation_constraints": device['lorawan_device']['activation_constraints'] if 'activation_constraints' in device.keys() else "local",
                                "app_eui": device['lorawan_device']['app_eui'],
                                "app_id": self.settings['TTN_APPLICATIONS'][to_app_id]['app_id'],
                                "app_key": device['lorawan_device']['app_key'],
                                "dev_eui": device['lorawan_device']['dev_eui'],
                                "dev_id": device['dev_id'],
                                "disable_f_cnt_check": False,
                                "f_cnt_down": device['f_cnt_down'] if 'f_cnt_down' in device.keys() else 0,
                                "f_cnt_up": device['f_cnt_up'] if 'f_cnt_up' in device.keys() else 0,
                                "last_seen": device['last_seen'] if 'last_seen' in device.keys() else 0,
                                "uses32_bit_f_cnt": True
                            }
                        }

        return migrate_device

    # Migrate a device from the migrate client to the default client  
    def __migrate_device(device, self, migrate_client, to_app_id):
        dev_id = device['dev_id']

        new_device = self.get_new_device(device, to_app_id)

        self.delete_device(dev_id,migrate_client)

        response = self.register_devices([new_device])
        
        return response

