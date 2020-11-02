# Adaptive City Program TTN Manager
ACP TTN Manager provides means to manage TTN application and devices. It supports the following functionalities;
1. Get details of the TTN Application
2. Get details of all the registered devices on any application
3. Get details of a specific device on any application
4. Register a set of new devices to the default application
5. Update settings of an existing device
6. Delete a device from any application
7. Migrate a set of devices from one application to another application

## Installation

Ensure that both the default application and the application from which devices are being migrated have the same `APP EUI`.

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
Create a `secrets/config.py` file with the following entries;

```
URL = "https://eu.thethings.network:8094/applications/"

TTN_APPLICATIONS = {
                        'app_id1' : {
                            'app_id' : "app_id1",
                            'access_key' : "accesskey1",
                            'app_eui' : "appeui1"
                        },

                        'app_id2' : {
                            'app_id' : "app_id2",
                            'access_key' : "accesskey2",
                            'app_eui' : "appeui2"
                        }
                    }
```
### Usage with your own python code
Import the ACPTTNManager class and use the following class methods for the required functionalities

1. `get_app_details()`: Return the TTN Application object
2. `get_all_devices(client)`: Return all devices registered on the specified client application. Uses default client if no client specified.
3. `get_device_details(device_id, client)`: Return the device object corresponding to 'device_id' on the specified client application. Uses default client if no client specified.
4. `register_devices(devices)`: Register all devices contained in the list 'devices'. All list elements should be dictionaries of the format defined at *https://www.thethingsnetwork.org/docs/applications/manager/api.html*. If device is already present then update device settings.
5. `delete_device(dev_id, client)`: Delete all devices whose dev_id are in 'dev_ids'.  Uses default client if no client specified. Delete all devices if no dev_ids specified.
6. `migrate_devices(dev_ids)`: Migrate a set of devices from a TTN application to the default application of the class. Migrate all devices if no dev_ids specified.

See the `test.py` file for examples.

### Using the provided script

usage: `./ttn_manager.sh [-h] [-a app_id [-r] [-rf filename] [-w filename] [-d acp_id] [-m from_app_id [-f filename]]]`

`-h`: Print the help page

`-a`: The `app_id` of the TTN application

`-r`: Read all the registered devices and print on stdout

`-rf filename`: Read all the registered devices and write to a file

`-w filename`: Register all devices in filename. If device already present then update settings as provided in the file.

`-d acp_id`: Delete the device with the `acp_id`

`-m from_app_id [-f filename]`: Migrate devices listed in filename from the `from_app_id` application to the one specified by `-a`. All devices to be
                                    migrated should have their acp_id in the file separated by commas. If no file specified, then migrate all devices.