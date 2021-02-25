from ACPTTNManagerV3 import ACPTTNManagerV3
import json
import sys

def load_settings():
    with open('secrets/settings_v3.json', 'r') as settings_file:
        settings_data = settings_file.read()

    # parse file
    settings = json.loads(settings_data)
    return settings

# manager = ACPTTNManager(load_settings(), 'vlab-sensor-network-2')

# app = manager.get_app_details()
# devices = manager.get_all_devices()
# device = manager.get_device_details("elsys-co2-041bab")
# manager.migrate_devices('vlab-sensor-network-2')

#manager = ACPTTNManagerV3(load_settings(), 'cambridgesensornetwork', '3')
manager = ACPTTNManagerV3(load_settings(), 'vlab-sensor-network')

app = manager.get_app_details()
devices = manager.get_all_devices()
# print(app)
print(devices)
# device = manager.get_device_details("elsys-co2-0520a7")
# device = manager.get_device_details("elsys-co2-041bab")
# print(device)
# manager.delete_device('test-device')
# manager.migrate_devices('vlab-sensor-network-2')

def write(manager, json_file, device_id=None):
    with open(json_file) as jfile:
        json_data = json.load(jfile)
        # We will track whether the ttn app was updated
        app_updated=False
        for json_id in json_data.keys():
            if device_id is None or device_id==json_id:
                app_updated=True
                ttn_settings = json_data[json_id]['ttn_settings'] 
                print(json_id,': ',manager.register_device(ttn_settings))
        if not app_updated:
            if device_id:
                print(f"TTN application not updated (--id {device_id} not found?)", file=sys.stderr)
            else:
                print("Warning: TTN application not updated.", file=sys.stderr)

# write(manager, 'device_v3.json')

# print(manager.delete_device('elsys-co2-045abc'))

# manager.migrate_devices('vlab-sensor-network-2')               
