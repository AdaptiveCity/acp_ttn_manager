from ACPTTNManager import ACPTTNManager
import json

def load_settings():
    with open('secrets/settings.json', 'r') as settings_file:
        settings_data = settings_file.read()

    # parse file
    settings = json.loads(settings_data)
    return settings

manager = ACPTTNManager(load_settings(), 'vlab-sensor-network-2')

app = manager.get_app_details()
devices = manager.get_all_devices()
device = manager.get_device_details("elsys-co2-041bab")
manager.migrate_devices('vlab-sensor-network-2')
