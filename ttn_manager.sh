#!/usr/bin/env python3

from ACPTTNManager import ACPTTNManager
import json
from datetime import datetime
import sys
import os
import argparse

def get_existing_device_details(json_file):
    existing_devices = {}
    try:
        with open(json_file) as jfile:
            json_data = json.load(jfile)
            for sensor in json_data.keys():
                existing_devices[sensor] = json_data[sensor]
    except:
        print('Empty or corrupted file')

    return existing_devices

######################################################################
# Build local 'device entry' from device information from TTN
# The TTN registration data will be placed in property "ttn_settings"
# and "acp_ts" will be added.
######################################################################
def set_device_entry(device, dev_id, version, existing_device=None):
    # Note ACP timestamps are STRINGS e.g. "1606639856.527631"
    acp_ts = '{:.6f}'.format(datetime.now().timestamp())
    device_entry = {}
    if existing_device != None:
        for key in existing_device.keys():
            device_entry[key] = existing_device[key]
        device_entry["acp_ts"] = acp_ts
        device_entry["ttn_settings"] = device        
    else:
        device_entry = {
                "acp_id": dev_id,
                "acp_ts": acp_ts,
                "ttn_settings": device
            }
    device_entry["ttn_settings"]["ttn_version"] = version
    return device_entry

####################################################################
# Read device information from TTN
####################################################################
def read(manager, json_file=None, device_id=None):
    # Here is the TTN read
    version = manager.client.version
    device_key = 'devices' if version == 2 else 'end_devices'
    if device_id:
        device = manager.get_device_details(device_id)
        devices = {}
        devices[device_key] = [ device ]
    else:
        devices = manager.get_all_devices()

    if len(devices) == 0:
        print("No registered devices",file=sys.stderr,flush=True)
        return

    if json_file == None:
        sensors = {}
        for device in devices[device_key]:
            if 'error' in device:
                print('Device read error from TTN: {}'.format(device), file=sys.stderr, flush=True)
            else:
                dev_id = device['dev_id'] if version == 2 else device['ids']['device_id']
                device_entry = set_device_entry(device, dev_id, version)
                sensors[dev_id] = device_entry
        print(json.dumps(sensors, indent=4))
    else:
        existing_devices = get_existing_device_details(json_file) if os.path.exists(json_file) else {}
        opfile = open(json_file, 'w')
        sensors = {}
        for device in devices[device_key]:
            dev_id = device['dev_id'] if version == 2 else device['ids']['device_id']
            existing_device = existing_devices[dev_id] if dev_id in existing_devices.keys() else None
            device_entry = set_device_entry(device, dev_id, version, existing_device)
            sensors[dev_id] = device_entry
        opfile.write(json.dumps(sensors, indent=4))
        print('File written')

####################################################################
# Register/Update devices on TTN settings
####################################################################
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

def delete(manager, acp_id):
    response = manager.delete_device(acp_id)
    if response == {}:
        print('Device deleted')
    else:
        print(response['error'],file=sys.stderr,flush=True)

####################################################################
# Migrate devices
####################################################################
def migrate(manager, from_app_id, acp_id_file=None):

    if acp_id_file == None:
        response = manager.migrate_devices(from_app_id)
    else:
        acp_id_list = []
        ip = open(acp_id_file)
        acp_ids = ip.read()
        acp_id_list = json.loads(acp_ids)['acp_ids']
        if len(acp_id_list) == 0:
            print('Empty file')
            return
        response = manager.migrate_devices(from_app_id, acp_id_list)
        ip.close()

    print(response)

####################################################################
# Load settings
####################################################################
def load_settings():
    with open('secrets/settings_v3.json', 'r') as settings_file:
        settings_data = settings_file.read()

    # parse file
    settings = json.loads(settings_data)
    return settings

####################################################################
# Setup command line argument parsing
####################################################################
def parse_init():
    parser = argparse.ArgumentParser(description='Import/export json data <-> TTN')

    parser.add_argument('-a', '--app_id',
                        nargs=1,
                        required=True,
                        metavar='<ttn app id>',
                        help='Application id of the TTN Application')

    parser.add_argument('-f', '--jsonfile',
                        required='--write' in sys.argv or '-w' in sys.argv,
                        metavar='<JSON filename>',
                        help='Filename for JSON sensor registration data to be written to.')

    parser.add_argument('--id',
                        metavar='<acp_id>',
                        help="Sensor identifier (e.g. 'ijl20-sodaq-ttn') to limit scope to only this sensor")

    # We will create an exclusive args group for the commands
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-r', '--ttnread',
                        action='store_true',
                        help='Read all the registered devices and print to a file if filename provided, else print to stdout')

    group.add_argument('-w', '--ttnwrite',
                        action='store_true',
                        help='Register all devices in filename. Provide the filename using -f or --jsonfile. If device already present then update settings as provided in the file.')

    group.add_argument('-d', '--delete',
                        metavar='<acp_id>',
                        help='Delete the device with the acp_id')

    group.add_argument('-m', '--migrate',
                        nargs=1,
                        metavar='<from_app_id>',
                        help='Migrate devices listed in filename from the from_app_id application to the one specified by -a. All devices to be migrated should have their acp_id in a jsonfile in the format {"acp_ids": ["elsys-co2-044abc","elsys-co2-043abc"]}. Provide the filename using -f or --jsonfile. If no file specified, then migrate all devices.')

    return parser


#########################################################################
#########################################################################
###### Main Program          ############################################
#########################################################################
#########################################################################

if __name__ == '__main__':

    parser = parse_init()
    args = parser.parse_args()

    app_id = args.app_id[0]
    settings = load_settings()

    manager = ACPTTNManager(settings, app_id)

    if args.ttnread:
        read(manager, args.jsonfile, args.id)

    elif args.ttnwrite:
        write(manager, args.jsonfile, args.id)

    elif args.delete:
        delete(manager, args.delete)

    elif args.migrate:
        if args.jsonfile:
            migrate(manager, args.migrate[0], args.jsonfile)
        else:
            migrate(manager, args.migrate[0])

    else:
        print(manager.get_app_details())
