from ACPTTNManager import ACPTTNManager
import json
from datetime import datetime, timezone
import dateutil.parser

def load_settings():
    with open('secrets/settings.json', 'r') as settings_file:
        settings_data = settings_file.read()

    # parse file
    settings = json.loads(settings_data)
    return settings

manager = ACPTTNManager(load_settings(), 'cambridge-net-3')

app = manager.get_app_details()
devices = manager.get_all_devices()

migrated, not_migrated = [], []
for device in devices['end_devices']:
    updated_time = device['updated_at']
    dt = dateutil.parser.isoparse(updated_time)
    last_seen = ((datetime.now(timezone.utc) - dt).seconds)/3600
    if last_seen > 2.0:
        not_migrated.append(device['ids']['device_id'])
    else:
        migrated.append(device['ids']['device_id'])

print(f'Seen ({len(migrated)}): ',migrated)
print('######################')
print(f'Not Seen ({len(not_migrated)}): ',not_migrated)

