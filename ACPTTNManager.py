import config
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
    client = Client(
                        config.URL + config.DEFAULT_APP_ID, 
                        {"Authorization": "Key "+config.DEFAULT_ACCESS_KEY, "Content-Type":"application/json"}
                )

    @classmethod
    def get_app_details(self):
        '''
        Return the TTN Application object
        '''
        response = requests.get(self.client.url,headers=self.client.headers)
        return response.json()

    @classmethod
    def get_all_devices(self, client=None):
        '''
        Return all devices registered on the specified client application
        client: The application client. Use the default application client if None
        '''
        if client == None:
            client = self.client
        response = requests.get(client.url+"/devices",headers=client.headers)

        return response.json()
        

    @classmethod
    def get_device_details(self, device_id, client=None):
        '''
        Return the device object corresponding to 'device_id' on the specified client application
        client: The application client. Use the default application client if None
        '''
        if client == None:
            client = self.client
        response = requests.get(client.url+"/devices/"+device_id,headers=client.headers)

        return response.json()

    @classmethod
    def register_new_devices(self, devices):
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
        

    @classmethod
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
    
    

    @classmethod
    def migrate_devices(self, dev_ids=None):
        '''
        Migrate a set of devices from a TTN application to the default application of the class
        dev_ids: List containing the dev_id of all the devices to be migrated. Migrate all devices if empty
        '''
        migrate_client = Client(
                                    url= config.URL + config.MIGRATE_APP_ID,
                                    headers={"Authorization": "Key "+config.MIGRATE_ACCESS_KEY, "Content-Type":"application/json"}
                            )
        response_list = []

        if dev_ids == None:            
            devices = self.get_all_devices(migrate_client)
            for device in devices['devices']:
                response = ACPTTNManager.__migrate_device(device, self, migrate_client)

                if response != 'Device added':
                    response_list.append(response)
        else:
            for dev_id in dev_ids:
                device = self.get_device_details(dev_id, migrate_client)
        
                response = ACPTTNManager.__migrate_device(device, self, migrate_client)

                if response != 'Device added':
                    response_list.append(response)

        if len(response_list) == 0:
            return "All devices migrated"
        else:
            return json.dumps(response_list)

    #Create a device dictionary
    def get_new_device(dev_eui, dev_id):
        migrate_device = {
                            "altitude": 0,
                            "app_id": config.DEFAULT_APP_ID,
                            "attributes": {
                                "key": "",
                                "value": ""
                            },
                            "description": "Some description of the device",
                            "dev_id": dev_id,
                            "latitude": 0.0,
                            "longitude": 0.0,
                            "lorawan_device": {
                                "activation_constraints": "local",
                                "app_eui": config.DEFAULT_APP_EUI,
                                "app_id": config.DEFAULT_APP_ID,
                                "app_key": config.MIGRATION_APP_KEY,
                                "dev_eui": dev_eui,
                                "dev_id": dev_id,
                                "disable_f_cnt_check": False,
                                "f_cnt_down": 0,
                                "f_cnt_up": 0,
                                "last_seen": 0,
                                "uses32_bit_f_cnt": True
                            }
                        }

        return migrate_device

    # Migrate a device from the migrate client to the default client
    
    def __migrate_device(device, self, migrate_client):
        dev_eui = device['lorawan_device']['dev_eui']
        dev_id = device['dev_id']

        self.delete_device(dev_id,migrate_client)

        new_device = self.get_new_device(dev_eui, dev_id)

        response = self.register_new_devices([new_device])
        
        return response

