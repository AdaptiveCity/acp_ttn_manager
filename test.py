from ACPTTNManager import ACPTTNManager
import json
from datetime import datetime

def load_settings():
    with open('secrets/settings.json', 'r') as settings_file:
        settings_data = settings_file.read()

    # parse file
    settings = json.loads(settings_data)
    return settings

manager = ACPTTNManager(load_settings(), 'cambridge-net-3')

app = manager.get_app_details()
devices = manager.get_all_devices()
            
for device in devices['end_devices']:
    updated_time = device['updated_at'][:-4]
    dt = datetime.strptime(updated_time, '%Y-%m-%dT%H:%M:%S.%f')
    last_seen = ((datetime.now() - dt).seconds)/3600
    if last_seen > 2.0:
        print(device['ids']['device_id'])