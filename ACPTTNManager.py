import config
import ttn
import binascii

class ACPTTNManager:
    ttn_handler = ttn.HandlerClient(config.DEFAULT_APP_ID, config.DEFAULT_ACCESS_KEY)
    app_client =  ttn_handler.application()

    @classmethod
    def get_app_details(self):
        '''
        Return the TTN Application object
        '''
        my_app = self.app_client.get()
        return(my_app)

    @classmethod
    def get_all_devices(self, client=None):
        '''
        Return all devices registered on the specified client application
        client: The application client. Use the default application if None
        '''
        if client == None:
            client = self.app_client
        my_devices = client.devices()
        return(my_devices)

    @classmethod
    def get_device_details(self, device_id, client=None):
        '''
        Return the device object corresponding to 'device_id' on the specified client application
        client: The application client. Use the default application if None
        '''
        if client == None:
            client = self.app_client
        return client.device(device_id)

    @classmethod
    def register_new_devices(self, devices):
        '''
        Register all devices contained in the list 'devices'
        devices: A list of device dictionaries of the form {'dev_id':dev_id, 'dev_details':{A dictionary of all device details}}
        '''
        for device in devices:
            self.app_client.register_device(device['dev_id'], device['dev_details'])

    @classmethod
    def delete_devices(self, dev_ids=None, client=None):
        '''
        Delete all devices whose dev_ids are in 'dev_ids'.
        dev_ids: List containing dev_id of the devices to be deleted. Delete all devices if None
        client: The TTN application client from which the devices should be removed. Default: Default TTN Application of the class
        '''
        if client == None:
            client = self.app_client

        if dev_ids == None:
            dev_ids = []
            all_devices = self.get_all_devices(client)
            for dev in all_devices:
                dev_ids.append(dev.dev_id)

        for dev_id in dev_ids:
            client.delete_device(dev_id)

    @classmethod
    def migrate_devices(self, from_app_id, from_access_key, migration_key, dev_ids=None):
        '''
        Migrate a set of devices from a TTN application to the default application of the class
        dev_ids: List containing the dev_id of all the devices to be migrated. Migrate all devices if empty
        from_app_id: Application Id of the application from which the devices are to be migrated
        from_access_key: Access key of the application from which the devices are to be migrated
        migration_key: App Key to be used for registering the device on the default application
        '''
        from_ttn_handler = ttn.HandlerClient(from_app_id, from_access_key)
        from_app_client = from_ttn_handler.application()

        if dev_ids == None:
            dev_ids = []
            all_devices = self.get_all_devices(from_app_client)
            for dev in all_devices:
                dev_ids.append(dev.dev_id)
        devices = []
        for dev_id in dev_ids:
            device = self.get_device_details(dev_id, from_app_client)
            devices.append({
                "dev_id" : dev_id, 
                "dev_details" : {
                    "appEui" : config.DEFAULT_APP_EUI,
                    "devEui" : binascii.b2a_hex(device.lorawan_device.dev_eui).upper(),
                    "appKey" : migration_key    
                }})

        self.delete_devices(dev_ids, from_app_client)
        
        self.register_new_devices(devices)
