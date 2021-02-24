# Adaptive City Program TTN Manager
This repo has been updated to support the changes made by the V3 transition. [V2 to V3 Changes](V2-V3_Changes.md)<br>
ACP TTN Manager provides means to manage TTN application and devices. It supports the following functionalities;
1. Get details of the TTN Application
2. Get details of all the registered devices on any application
3. Get details of a specific device on any application
4. Register a set of new devices to the default application
5. Update settings of an existing device
6. Delete a device from any application
7. Migrate a set of devices from one application to another application

## Installation

Use ttn_manager_v3.sh which supports TTN V3.

You would need Python 3 for running.

```
git clone https://github.com/AdaptiveCity/acp_ttn_manager.git
cd acp_ttn_manager
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pip --upgrade
python3 -m pip install wheel
python3 -m pip install -r requirements.txt
```

## Usage
Create a `secrets/settings_v3.json` file with the following entries;

```
{
    "SERVER_ADDRESS": "eu.ttn.example.com",
    "FREQUENCY_PLAN": "EU_863_870_TTN",
    "LORAWAN_VERSION": "1.0.3",
    "URLS" : {
        "2" : {
            "url" : "https://eu.ttn.example.com:8094/applications/"           
        },
        "3" : {
            "url" : "https://eu1.ttn.example.com/api/v3/applications/"            
        }

    },
    "TTN_APPLICATIONS" : {
                        "appid1" : {
                            "version":2,
                            "auth_type": "Key",
                            "app_id" : "appid1",
                            "access_key" : "key",
                            "app_eui" : "0000000000000000"
                        },

                        "appid" : {
                            "version":3,
                            "auth_type": "Bearer",
                            "app_id" : "appid",
                            "access_key" : "key"
                        }
                    },
    "ID_SERVER_MASKS":{
        "paths":[
            "join_server_address",
            "network_server_address",
            "application_server_address",
            "ids.dev_eui",
            "ids.join_eui",
            "name"
         ]
    },
    "NETWORK_SERVER_MASKS":{
        "paths":[
           "multicast",
           "supports_join",
           "lorawan_version",
           "mac_settings.supports_32_bit_f_cnt",
           "supports_class_c",
           "supports_class_b",
           "lorawan_phy_version",
           "frequency_plan_id"
        ]
    },
    "JOIN_SERVER_MASKS":{
        "paths":[
           "network_server_kek_label",
           "application_server_kek_label",
           "application_server_id",
           "net_id",
           "root_keys.app_key.key"
        ]
     }
}
```
### Usage with your own python code
Import the ACPTTNManager class and use the following class methods for the required functionalities

1. `get_app_details()`: Return the TTN Application object
2. `get_all_devices(client)`: Return all devices registered on the specified client application. Uses default client if no client specified.
3. `get_device_details(device_id, client)`: Return the device object corresponding to 'device_id' on the specified client application. Uses default client if no client specified.
4. `register_device(device_settings)`: Register a device with the details provided in device_settings. If device is already present then update device settings.
5. `delete_device(dev_id, client)`: Delete all devices whose dev_id are in 'dev_ids'.  Uses default client if no client specified. Delete all devices if no dev_ids specified.
6. `migrate_devices(dev_ids)`: Migrate a set of devices from a TTN application to the default application of the class. Migrate all devices if no dev_ids specified.

See the `test.py` file for examples.

### Using the provided script

usage:
```
./ttn_manager.sh [--help] --app_id APP_ID --ttn_version TTN VERSION
        [--ttnread | --ttnwrite | --delete <acp_id> | --migrate <from_app_id>] [--jsonfile JSONFILE]
        [--id <acp_id>]

Import/export json data <-> TTN

optional arguments:

  --help: show this help message and exit

  --app_id <APP_ID>: Application id of the TTN Application

  --ttn_version <TTN VERSION>: TTN Version Number

  --ttnread: Read all the registered devices and print to a file if filename provided, else
             print to stdout

  --ttnwrite: Register all devices in filename. Provide the filename using -f or --jsonfile.
              If device already present then update settings as provided in the file.

  --delete <acp_id>: Delete the device with the acp_id

  --migrate <from_app_id>: Migrate devices listed in filename from the from_app_id application to
             the one specified by -a. All devices to be migrated should have their acp_id in a
             jsonfile in the format listed below. Provide the filename using -f or --jsonfile.
             If no file specified, then migrate all devices.

  --jsonfile <JSONFILE>: Filename for the command requesting a file

  --id <acp_id>`: limits scope of command to a given TTN device id.
```

## Examples

```
cd ~/acp_ttn_manager
source venv/bin/activate
```

In all these examples the uploaded/downloaded information will look like:
<br> V2 device
```
{
    "elsys-co2-045xxx": {
        "acp_id": "elsys-co2-045xxx",
        "acp_ts": "1606644010.042376",
        "ttn_settings": {
            "app_id": "vlab-sensor-network",
            "dev_id": "elsys-co2-045xxx",
            "lorawan_device": {
                "app_eui": "70B3D57ED00358FF",
                "dev_eui": "A81758FFFE046777",
                "app_id": "vlab-sensor-network",
                "dev_id": "elsys-co2-045xxx",
                "dev_addr": "",
                "nwk_s_key": "",
                "app_s_key": "",
                "app_key": "22C905D1A45D1EEED8D950B915ECC8D8",
                "uses32_bit_f_cnt": true,
                "activation_constraints": "local"
            },
            "attributes": {
                "key": "",
                "value": ""
            }
        }
    }
    ... followed by similar device entries
}
```
<br> V3 device
```
"elsys-co2-045xxx": {
        "acp_id":"elsys-co2-045xxx",
        "acp_ts":1604930667.132143,
        "ttn_settings":{
           "ids":{
              "device_id":"elsys-co2-045xxx",
              "application_ids":{
                 "application_id":"vlab-sensor-network"
              },
              "dev_eui":"A81758FFFE045xxx",
              "join_eui":"70B3D57ED00358FF"
           },
           "created_at":"0001-01-01T00:00:00Z",
           "updated_at":"0001-01-01T00:00:00Z",
           "name":"elsys-co2-043abc",
           "description":"Elsys Test Device",
           "attributes":{
              "key":"",
              "value":""
           },
           "lorawan_version":"1.0.3",
           "lorawan_phy_version":"1.0.3-a",
           "frequency_plan_id":"EU_863_870_TTN",
           "supports_join":true,
           "root_keys":{
              "app_key":{
                 "key":"22C905D1A45D1EAED8D950B915ECC8D8"
              }
           },
           "mac_settings":{
              "rx1_delay":{
                 "value":1
              },
              "supports_32_bit_f_cnt":true
           }
        }
    }
```

### Download all TTN device registrations for an application to stdout

```
./ttn_manager_v3.sh --ttnread --app_id vlab-sensor-network --ttn_version 2
```

### Download all TTN device registrations for an application to a file

```
./ttn_manager_v3.sh --ttnread --app_id vlab-sensor-network  --ttn_version 2 --jsonfile vlab_devices.json
```

**Note that if `vlab_devices.json` already exists, then the TTN settings will be MERGED
into that file **

### Download TTN registration data for a single device

```
./ttn_manager_v3.sh --ttnread --app_id vlab-sensor-network --ttn_version 2 --id elsys-co2-045xxx
```

A `--jsonfile` parameter can also be give, as in the prior example.

### Upload device registrations to TTN (i.e. register devices to an application)

```
./ttn_manager_v3.sh --ttnwrite --app_id vlab-sensor-network --ttn_version 2 --jsonfile my_devices.json
```

### Upload a single device registration to TTN (i.e. register a single device)

```
./ttn_manager_v3.sh --ttnwrite --app_id vlab-sensor-network --ttn_version 2 --jsonfile my_devices.json --id elsys-co2-045xxx
```

### Migrate all devices from one TTN application to another

```
./ttn_manager_v3.sh --migrate vlab-sensor-network --app_id my-new-app --ttn_version 2
```

### Migrate selected devices from one TTN application to another

```
./ttn_manager_v3.sh --migrate vlab-sensor-network --app_id my-new-app --ttn_version 2 --jsonfile device_ids.json
```

Where `device_ids.json` could be:
```
{
    "acp_ids": [
        "elsys-co2-044abc",
        "elsys-co2-043abc"
    ]
}
```
