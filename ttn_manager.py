from requests.models import Response
from ACPTTNManager import ACPTTNManager
import json
from datetime import datetime
import sys

def get_existing_device_details(json_file):
    existing_devices = {}
    with open(json_file) as jfile:
        json_data = json.load(jfile)
        for sensor in json_data['sensors']:
            existing_devices[sensor[list(sensor.keys())[0]]['acp_id']] = sensor[list(sensor.keys())[0]]

    return existing_devices

def set_device_entry(device, existing_device=None):
    split_dev_id = device['dev_id'].split('-')
    # print(split_dev_id)
    device_type = split_dev_id[0]+'-'+split_dev_id[1]
    acp_ts = datetime.now().timestamp()
    device_entry = ''
    if existing_device != None:
        device_entry = {
            device['dev_id']:{
                "acp_id": device['dev_id'],
                "acp_type_id": existing_device['acp_type_id'] if 'acp_type_id' in existing_device.keys() else device_type,
                "acp_ts": acp_ts,
                "crate_id": existing_device['crate_id'] if 'crate_id' in existing_device.keys() else "",
                "acp_location": existing_device['acp_location'] if 'acp_location' in existing_device.keys() else {
                    "x": 0,
                    "y": 0,
                    "zf": 0,
                    "f": 0,
                    "system": "WGB"
                },
                "ttn_settings": device
            }
        }
    else:
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

def read(manager, json_file=None):
    devices = manager.get_all_devices()

    if json_file == None:
        sensors = {'sensors':[]}
        for device in devices['devices']:
            device_entry = set_device_entry(device)
            sensors['sensors'].append(device_entry)
        print(json.dumps(sensors, indent=4))
    else:
        existing_devices = get_existing_device_details(json_file)
        opfile = open(json_file, 'w')
        sensors = {'sensors':[]}
        for device in devices['devices']:
            existing_device = existing_devices[device['dev_id']] if device['dev_id'] in existing_devices.keys() else None
            device_entry = set_device_entry(device, existing_device)
            sensors['sensors'].append(device_entry)
        opfile.write(json.dumps(sensors, indent=4))

def write(manager, json_file):

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
            print(manager.register_new_devices([device]))

def delete(manager, acp_id):
    response = manager.delete_device(acp_id)
    if response == {}:
        print('Device deleted')

def migrate(manager, from_app_id, acp_id_file=None):

    if acp_id_file == None:
        response = manager.migrate_devices(from_app_id)
    else:
        acp_id_list = []
        ip = open(acp_id_file)
        acp_id_list = ip.readlines()[0].strip().split(',')
        response = manager.migrate_devices(from_app_id, acp_id_list)
        ip.close()

    print(response)

def help():
    ip = open('commands.txt')
    for eachline in ip:
        print(eachline.strip())
    ip.close()

if __name__ == '__main__':
    command_list = ['-h', '-a', '-r', '-rf', '-w', '-d', '-m', '-f']
    command_dict = {}

    if sys.argv[1] == '-h':
        help()
    else:
        i = 1
        while i < len(sys.argv):
            command = sys.argv[i]
            if command in command_list:
                try:
                    command_dict[command] = sys.argv[i+1]
                except IndexError:
                    if command == '-r':
                        command_dict[sys.argv[i]] = ''
                    else:
                        print('Incorrect Command')
                        help()
                        exit()
            else:
                print('Incorrect Command')
                help()
                exit()
            i+=2
    
        if '-a' not in command_dict.keys():
            print('Need Application id')
            help()
        else:
            manager = ACPTTNManager(command_dict['-a'])

            if '-r' in command_dict.keys():
                read(manager)
            elif '-rf' in command_dict.keys():
                read(manager, command_dict['-rf'])
            elif '-w' in command_dict.keys():
                write(manager, command_dict['-w'])
            elif '-d' in command_dict.keys():
                delete(manager, command_dict['-d'])
            elif '-m' in command_dict.keys():
                if '-f' in command_dict.keys():
                    migrate(manager, command_dict['-m'], command_dict['-f'])
                else:
                    migrate(manager, command_dict['-m'])

