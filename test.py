from ACPTTNManager import ACPTTNManager
import config

manager = ACPTTNManager()

app = manager.get_app_details()
devices = manager.get_all_devices()
device = manager.get_device_details("elsys-co2-041bab")

# manager.migrate_devices(['elsys-co2-041bab'], config.MIGRATE_APP_ID, config.MIGRATE_ACCESS_KEY, config.MIGRATION_APP_KEY)