# Adaptive City Program TTN Manager
(More testing needed)
ACP TTN Manager provides means to manage TTN application and devices. It supports the following functionalities;
1. Get details of the TTN Application
2. Get details of all the registered devices on any application
3. Get details of a specific device on any application
4. Register a set of new devices to the default application
5. Delete a set of devices from any application
6. Migrate a set of devices from any application to the default application

## Installation

Ensure that both the default and the application from which devices are being migrated have the same `APP EUI`.

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
Create a `config.py` file with the following entries;

```
DEFAULT_APP_ID = ""
DEFAULT_ACCESS_KEY = ""
DEFAULT_APP_EUI = ""

# Details of application from which migrating
MIGRATE_APP_ID = ""
MIGRATE_ACCESS_KEY = ""
MIGRATION_APP_KEY = ""
```

Import the ACPTTNManager class and use the following class methods for the required functionalities

1. `get_app_details()`: Return the TTN Application object
2. `get_all_devices(client)`: Return all devices registered on the specified client application. Uses default client if no client specified.
3. `get_device_details(device_id, client)`: Return the device object corresponding to 'device_id' on the specified client application. Uses default client if no client specified.
4. `register_new_devices(devices)`: Register all devices contained in the list 'devices'. All list elements should be dictionaries of the format `{'dev_id':dev_id, 'dev_details':{A dictionary of all device details. Must contain "appEui", "devEui", "appKey"}}`. All device details keys available at *https://www.thethingsnetwork.org/docs/applications/python/api-reference.html*
5. `delete_devices(dev_ids, client)`: Delete all devices whose dev_id are in 'dev_ids'.  Uses default client if no client specified. Delete all devices if no dev_ids specified.
6. `migrate_devices(from_app_id, from_access_key, migration_key, dev_ids)`: Migrate a set of devices from a TTN application to the default application of the class. Migrate all devices if no dev_ids specified.

See the `test.py` file for examples.