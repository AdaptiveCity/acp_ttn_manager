## Get device:
### With Mask
Call: https://eu1.cloud.thethings.network/api/v3/js/applications/cambridgesensornetwork/devices/elsys-co2-041abc?field_mask=resets_join_nonces,network_server_address,application_server_address,net_id,application_server_id,application_server_kek_label,network_server_kek_label,claim_authentication_code,root_keys

Response: {"ids":{"device_id":"elsys-co2-041abc","application_ids":{"application_id":"cambridgesensornetwork"},"dev_eui":"A81758FFFE042BAB","join_eui":"70B3D57ED00358FE"},"created_at":"2021-02-15T15:29:19.375409749Z","updated_at":"2021-02-15T15:29:19.375409749Z","network_server_address":"eu1.cloud.thethings.network","application_server_address":"eu1.cloud.thethings.network","root_keys":{"app_key":{"key":"22C905D1A45D1EAED8D950B915ECC8D8"}}}

### Without Mask
Call: https://eu1.cloud.thethings.network/api/v3/applications/cambridge-net-3/devices/elsys-co2-0520a7
Response: {'ids': {'device_id': 'elsys-co2-0520a7', 'application_ids': {'application_id': 'cambridge-net-3'}, 'dev_eui': 'A81758FFFE0520A7', 'join_eui': '70B3D57ED00358FF'}, 'created_at': '2021-02-15T18:19:14.524Z', 'updated_at': '2021-02-15T18:19:14.524Z'}

## Get devices:
Call: https://eu1.cloud.thethings.network/api/v3/applications/cambridgesensornetwork/devices

Response: {"end_devices":[{"ids":{"device_id":"elsys-co2-041abc","application_ids":{"application_id":"cambridgesensornetwork"},"dev_eui":"A81758FFFE042BAB","join_eui":"70B3D57ED00358FE"},"created_at":"2021-02-15T15:29:19.220Z","updated_at":"2021-02-15T15:29:19.220Z","name":"elsys-co2-041abc"},{"ids":{"device_id":"elsys-co2-042abc","application_ids":{"application_id":"cambridgesensornetwork"},"dev_eui":"A81758FFFE043BAB","join_eui":"70B3D57ED00358FF"},"created_at":"2021-02-15T15:33:35.043Z","updated_at":"2021-02-15T15:33:35.043Z","name":"elsys-co2-042abc"},{"ids":{"device_id":"elsys-co2-043abc","application_ids":{"application_id":"cambridgesensornetwork"},"dev_eui":"A81758FFFE044BAB","join_eui":"70B3D57ED00358FF"},"created_at":"2021-02-15T15:36:27.094Z","updated_at":"2021-02-15T15:36:27.094Z","name":"elsys-co2-043abc"},{"ids":{"device_id":"elsys-co2-044abc","application_ids":{"application_id":"cambridgesensornetwork"},"dev_eui":"A81758FFFE045BAB","join_eui":"70B3D57ED00358FF"},"created_at":"2021-02-15T15:36:27.418Z","updated_at":"2021-02-15T15:36:27.418Z","name":"elsys-co2-044abc"},{"ids":{"device_id":"elsys-co2-045abc","application_ids":{"application_id":"cambridgesensornetwork"},"dev_eui":"A81758FFFE046BAB","join_eui":"70B3D57ED00358FF"},"created_at":"2021-02-15T15:36:27.730Z","updated_at":"2021-02-15T15:36:27.730Z","name":"elsys-co2-045abc"},{"ids":{"device_id":"test-device","application_ids":{"application_id":"cambridgesensornetwork"},"dev_eui":"A81758FFFE041EAE","join_eui":"70B3D57ED001AB65"},"created_at":"2021-02-15T11:00:51.803Z","updated_at":"2021-02-15T11:00:51.803Z","name":"Test device"}]}


## Register device:
1. Call: https://eu1.cloud.thethings.network/api/v3/applications/cambridgesensornetwork/devices
POST: {"end_device":{"ids":{"device_id":"test-device-1","dev_eui":"A81758FFFE044BAB","join_eui":"70B3D57ED00358FF"},"join_server_address":"eu1.cloud.thethings.network","network_server_address":"eu1.cloud.thethings.network","application_server_address":"eu1.cloud.thethings.network","name":"test device"},"field_mask":{"paths":["join_server_address","network_server_address","application_server_address","ids.dev_eui","ids.join_eui","name"]}}

2. Call: https://eu1.cloud.thethings.network/api/v3/ns/applications/cambridgesensornetwork/devices/test-device-1
PUT: {"end_device":{"multicast":false,"supports_join":true,"lorawan_version":"1.0.3","ids":{"device_id":"test-device-1","dev_eui":"A81758FFFE044BAB","join_eui":"70B3D57ED00358FF"},"mac_settings":{"supports_32_bit_f_cnt":true},"supports_class_c":false,"supports_class_b":false,"lorawan_phy_version":"1.0.3-a","frequency_plan_id":"EU_863_870_TTN"},"field_mask":{"paths":["multicast","supports_join","lorawan_version","ids.device_id","ids.dev_eui","ids.join_eui","mac_settings.supports_32_bit_f_cnt","supports_class_c","supports_class_b","lorawan_phy_version","frequency_plan_id"]}}

3. Call: https://eu1.cloud.thethings.network/api/v3/as/applications/cambridgesensornetwork/devices/test-device-1
PUT: {"end_device":{"ids":{"device_id":"test-device-1","dev_eui":"A81758FFFE044BAB","join_eui":"70B3D57ED00358FF"}},"field_mask":{"paths":["ids.device_id","ids.dev_eui","ids.join_eui"]}}

4. Call: https://eu1.cloud.thethings.network/api/v3/js/applications/cambridgesensornetwork/devices/test-device-1
PUT: {"end_device":{"ids":{"device_id":"test-device-1","dev_eui":"A81758FFFE044BAB","join_eui":"70B3D57ED00358FF"},"network_server_address":"eu1.cloud.thethings.network","application_server_address":"eu1.cloud.thethings.network","network_server_kek_label":"","application_server_kek_label":"","application_server_id":"","net_id":null,"root_keys":{"app_key":{"key":"22C905D1A45D1EAED8D950B915ECC8D8"}}},"field_mask":{"paths":["network_server_address","application_server_address","ids.device_id","ids.dev_eui","ids.join_eui","network_server_kek_label","application_server_kek_label","application_server_id","net_id","root_keys.app_key.key"]}}

## Delete device:
1. Call: https://eu1.cloud.thethings.network/api/v3/as/applications/cambridgesensornetwork/devices/test-device-1
2. Call: https://eu1.cloud.thethings.network/api/v3/js/applications/cambridgesensornetwork/devices/test-device-1
3. Call: https://eu1.cloud.thethings.network/api/v3/ns/applications/cambridgesensornetwork/devices/test-device-1
4. Call: https://eu1.cloud.thethings.network/api/v3/applications/cambridgesensornetwork/devices/test-device-1