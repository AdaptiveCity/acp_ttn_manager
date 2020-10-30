from ACPTTNManager import ACPTTNManager

manager = ACPTTNManager('vlab-sensor-network')

app = manager.get_app_details()

devices = manager.get_all_devices()
device = manager.get_device_details("elsys-co2-041bab")
manager.migrate_devices()