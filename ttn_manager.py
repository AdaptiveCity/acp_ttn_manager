from requests.models import Response
from ACPTTNManager import ACPTTNManager
import json
from datetime import datetime
import sys
import os
import argparse

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
        existing_devices = get_existing_device_details(json_file) if os.path.exists(json_file) else {}
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
    if len(devices) > 0:
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
            print(manager.register_devices([device]))

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

####################################################################
# Load settings
####################################################################
def load_settings():
    with open('secrets/settings.json', 'r') as settings_file:
        settings_data = settings_file.read()

    # parse file
    settings = json.loads(settings_data)
    return settings

def parse_init():
    parser = argparse.ArgumentParser(description='Import/export json data <-> TTN')
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-a', '--app_id',
                        nargs=1,
                        required=True,
                        help='Application id of the TTN Application')

    group.add_argument('-r', '--read',
                        action='store_true',
                        help='Read all the registered devices and print to a file if filename provided, else print to stdout')

    group.add_argument('-w', '--write',
                        action='store_true',
                        help='Register all devices in filename. Provide the filename using -f or --filename. If device already present then update settings as provided in the file.')

    group.add_argument('-d', '--delete',
                        nargs=1,
                        metavar='acp_id',
                        help='Delete the device with the acp_id')

    group.add_argument('-m', '--migrate',
                        nargs=1,
                        metavar='from_app_id',
                        help='Migrate devices listed in filename from the from_app_id application to the one specified by -a. All devices to be migrated should have their acp_id in a file separated by commas. Provide the filename using -f or --filename. If no file specified, then migrate all devices.')

    parser.add_argument('-f', '--filename',
                        nargs=1,
                        required='--write' in sys.argv or '-w' in sys.argv,
                        help='Filename for the command')

    return parser

if __name__ == '__main__':

    parser = parse_init()
    args = parser.parse_args()

    app_id = args.app_id[0]

    settings = load_settings()

    manager = ACPTTNManager(settings, app_id)

    if args.read:
        if args.filename:
            read(manager, args.filename[0])
        else:
            read(manager)

    elif args.write:
        write(manager, args.filename[0])

    elif args.delete:
        delete(manager, args.delete[0])

    elif args.migrate:
        if args.filename:
            migrate(manager, args.migrate[0], args.filename[0])
        else:
            migrate(manager, args.migrate[0])
