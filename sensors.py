from ACPTTNManager import ACPTTNManager
import json
from datetime import datetime
import sys

manager = ACPTTNManager()

def set_device_entry(device):
    split_dev_id = device['dev_id'].split('-')
    # print(split_dev_id)
    device_type = split_dev_id[0]+'-'+split_dev_id[1]
    acp_ts = datetime.now().timestamp()
    device_entry = {
        device['dev_id']:{
            "acp_id": device['dev_id'],
            "acp_type_id": device_type,
            "acp_ts": acp_ts,
            "crate_id": "",
            "acp_location": {
                "x": 0,
                "y": 0,
                "zf": 0,
                "f": 0,
                "system": "WGB"
            },
            "ttn_settings": device
        }
    }
    return device_entry

def read(json_file=None):
    devices = manager.get_all_devices()

    if json_file == None:
        sensors = {'sensors':[]}
        for device in devices['devices']:
            device_entry = set_device_entry(device)
            sensors['sensors'].append(device_entry)
        print(json.dumps(sensors, indent=4))
    else:
        opfile = open(json_file, 'w')
        sensors = {'sensors':[]}
        for device in devices['devices']:
            device_entry = set_device_entry(device)
            sensors['sensors'].append(device_entry)
        opfile.write(json.dumps(sensors, indent=4))

def write(json_file):

    devices = manager.get_all_devices()
    dev_id_list = []
    for device in devices['devices']:
        dev_id_list.append(device['dev_id'])

    with open(json_file) as jfile:
        json_data = json.load(jfile)
        for sensor in json_data['sensors']:
            ttn_settings = sensor[list(sensor.keys())[0]]['ttn_settings']
            device = {
                "altitude": ttn_settings['altitude'] if 'altitude' in ttn_settings.keys() else 0,
                "app_id": ttn_settings['app_id'],
                "attributes": ttn_settings['attributes'] if 'attributes' in ttn_settings.keys() else {"key": "","value": ""},
                "description": ttn_settings['description'] if 'description' in ttn_settings.keys() else "",
                "dev_id": ttn_settings['dev_id'],
                "latitude": ttn_settings['latitude'] if 'latitude' in ttn_settings.keys() else 0.0,
                "longitude": ttn_settings['longitude'] if 'longitude' in ttn_settings.keys() else 0.0,
                "lorawan_device": ttn_settings['lorawan_device']
            }
            if device['dev_id'] in dev_id_list:
                print('device', device['dev_id'], 'already registered')
            else:
                print(manager.register_new_devices([device]))
                # print('device', device['dev_id'], 'successfully registered')

def delete(acp_id):
    response = manager.delete_device(acp_id)
    if response == {}:
        print('Device deleted')

if __name__ == '__main__':
    command = sys.argv[1]    

    if command == 'read':
        filename = None
        try:
            filename = sys.argv[2]
        except:
            pass
        read(filename)

    elif command == 'write':
        filename = None
        try:
            filename = sys.argv[2]
        except:
            pass

        if filename == None:
            print('Filename required')
        else:
            write(filename)

    elif command == 'delete':
        acp_id = None

        try:
            acp_id = sys.argv[2]
        except:
            pass

        if acp_id == None:
            print('Device id required')
        else:
            delete(acp_id)

