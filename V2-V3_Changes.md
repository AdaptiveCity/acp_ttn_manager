Listed below are the major changes while migrating from V2 to V3.

### Multiple Device Registries
TTN V3 has introduced four device registries on which the device could be registered. For our purpose, we would need to register on all four. The devices should be registered in the order as below.
1. Identity Server: This is the mandatory registry which includes the default device information like ids, name, description, location, **picture**, and the other registry server addresses as described next.
2. Join Server: This is only required for OTAA devices. It includes the necessary application and network keys along with labels and addresses of the following two servers.
3. Network Server: This includes the network related information like lorawan version, freqency plans, mac information, mulitcast information and session keys.
4. Application Server: This could simply work with the ids for registration. The session information, which this registry stores, for applications trying to connect with a device are dynamic.

### New/Renamed Fields
Many of the hidden fields in V2 are explicitly required here and several have been renamed. These are listed below;
<br>Renamed:
```
app_id -> not applicable
dev_id -> ids.device_id
lorawan_device.dev_eui -> ids.dev_eui
lorawan_device.app_eui -> ids.join_eui
lorawan_device.dev_eui.app_key -> root_keys.app_key.key
```
Added:
```
lorawan_version, lorawan_phy_version, frequency_plan_id, supports_join, mac_settings, name, *.server_address
```
Below is an example of two CO2 devices registered on V2 and V3.<br>
V2:
```
{
    "app_id": "vlab-sensor-network",
    "dev_id": "elsys-co2-041abc",
    "lorawan_device": {
        "app_eui": "70B3D57ED00358FE",
        "dev_eui": "A81758FFFE042BAB",
        "app_id": "vlab-sensor-network",
        "dev_id": "elsys-co2-041abc",
        "dev_addr": "",
        "nwk_s_key": "",
        "app_s_key": "",
        "app_key": "22C905D1A45D1EAED8D950B915ECC8D8",
        "uses32_bit_f_cnt": true,
        "activation_constraints": "local"
    },
    "attributes": {
        "key": "",
        "value": ""
    },
    "description": "New Description"
}
```
V3:
```
{
    "ids": {
        "device_id": "elsys-co2-0520a7",
        "application_ids": {
            "application_id": "cambridge-net-3"
        },
        "dev_eui": "A81758FFFE0520A7",
        "join_eui": "70B3D57ED00358FF",
        "dev_addr": "260B6F30"
    },
    "created_at": "2021-02-15T18:19:14.713108373Z",
    "updated_at": "2021-02-22T18:01:44.744953482Z",
    "name": "Elsys CO2 0520A7",
    "network_server_address": "eu1.cloud.thethings.network",
    "application_server_address": "eu1.cloud.thethings.network",
    "join_server_address": "eu1.cloud.thethings.network",
    "root_keys": {
        "app_key": {
            "key": "22C905D1A45D1EAED8D950B915ECC8D8"
        }
    },
    "lorawan_version": "1.0.3",
    "lorawan_phy_version": "1.0.3-a",
    "frequency_plan_id": "EU_863_870_TTN",
    "supports_join": true,
    "mac_settings": {
        "supports_32_bit_f_cnt": true
    }
}
```

### Reading Device Data
1. In V2 this involved a single get call to obtain all available information of a device or a set of devices. An example call is *https://eu.thethings.network:8094/applications/devices*, which would return all devices of an application.
2. In V3 this involves three separate calls to the Idendity, Join and Network server to get all the information. An example set of calls would be
```
https://eu1.cloud.thethings.network/api/v3/applications/cambridge-net-3/devices/
https://eu1.cloud.thethings.network/api/v3/js/applications/cambridge-net-3/devices/<device-id>
https://eu1.cloud.thethings.network/api/v3/ns/applications/cambridge-net-3/devices/<device-id>
```
Note that the join and network server URL appends 'js' and 'ns' in between the URL and also is called for a specific device not for all devices at once. Also, the application id needs to be in the URL itself.
3. However, the default call as above would only return the ids and creation time information for the devices. Field Masks are introduces which need to be specified in order to get all information. These masks are;
```
Identity: "join_server_address", "network_server_address", "application_server_address", "ids.dev_eui", "ids.join_eui", "name"
Join: "multicast", "supports_join", "lorawan_version", "mac_settings.supports_32_bit_f_cnt", "supports_class_c", "supports_class_b", "lorawan_phy_version", "frequency_plan_id"
Network: "network_server_kek_label", "application_server_kek_label", "application_server_id", "net_id", "root_keys.app_key.key"
```
So an example call would be
```
https://eu1.cloud.thethings.network/api/v3/js/applications/cambridgesensornetwork/devices/elsys-co2-041abc?field_mask=resets_join_nonces,network_server_address,application_server_address,net_id,application_server_id,application_server_kek_label,network_server_kek_label,claim_authentication_code,root_keys
```
4. When queried for multiple devices, the key for V2 was `devices` while it is `end_devices` for V3.

### Registering Devices
1. V2 had a single registration POST call of the form *https://eu.thethings.network:8094/applications/devices* with the POST data being;
```
{
    "app_id": "vlab-sensor-network-2",
    "dev_id": "elsys-co2-041abc",
    "lorawan_device": {
        "app_eui": "70B3D57ED00358FE",
        "dev_eui": "A81758FFFE042BAB",
        "app_id": "vlab-sensor-network-2",
        "dev_id": "elsys-co2-041abc",
        "dev_addr": "",
        "nwk_s_key": "",
        "app_s_key": "",
        "app_key": "22C905D1A45D1EAED8D950B915ECC8D8",
        "uses32_bit_f_cnt": true,
        "activation_constraints": "local"
    },
    "attributes": {
        "key": "",
        "value": ""
    },
    "description": "New Description"
}
```
2. V3 requires four registrations in the order Identity>Join>Network>Application. The identity server call is POST while the other three are PUT. The example calls are as follows:
<br>Identity Server:
```
URL: https://eu1.cloud.thethings.network/api/v3/applications/cambridgesensornetwork/devices

{
  "end_device": {
    "ids": {
      "device_id": "test-device-1",
      "dev_eui": "A81758FFFE044BAB",
      "join_eui": "70B3D57ED00358FF"
    },
    "join_server_address": "eu1.cloud.thethings.network",
    "network_server_address": "eu1.cloud.thethings.network",
    "application_server_address": "eu1.cloud.thethings.network",
    "name": "test device"
  },
  "field_mask": {
    "paths": [
      "join_server_address",
      "network_server_address",
      "application_server_address",
      "ids.dev_eui",
      "ids.join_eui",
      "name"
    ]
  }
}
```
Join Server:
```
URL: https://eu1.cloud.thethings.network/api/v3/js/applications/cambridgesensornetwork/devices/test-device-1

{
  "end_device": {
    "ids": {
      "device_id": "test-device-1",
      "dev_eui": "A81758FFFE044BAB",
      "join_eui": "70B3D57ED00358FF"
    },
    "network_server_address": "eu1.cloud.thethings.network",
    "application_server_address": "eu1.cloud.thethings.network",
    "network_server_kek_label": "",
    "application_server_kek_label": "",
    "application_server_id": "",
    "net_id": null,
    "root_keys": {
      "app_key": {
        "key": "22C905D1A45D1EAED8D950B915ECC8D8"
      }
    }
  },
  "field_mask": {
    "paths": [
      "network_server_address",
      "application_server_address",
      "ids.device_id",
      "ids.dev_eui",
      "ids.join_eui",
      "network_server_kek_label",
      "application_server_kek_label",
      "application_server_id",
      "net_id",
      "root_keys.app_key.key"
    ]
  }
}
```
Network Server:
```
URL: https://eu1.cloud.thethings.network/api/v3/ns/applications/cambridgesensornetwork/devices/test-device-1
{
  "end_device": {
    "multicast": false,
    "supports_join": true,
    "lorawan_version": "1.0.3",
    "ids": {
      "device_id": "test-device-1",
      "dev_eui": "A81758FFFE044BAB",
      "join_eui": "70B3D57ED00358FF"
    },
    "mac_settings": {
      "supports_32_bit_f_cnt": true
    },
    "supports_class_c": false,
    "supports_class_b": false,
    "lorawan_phy_version": "1.0.3-a",
    "frequency_plan_id": "EU_863_870_TTN"
  },
  "field_mask": {
    "paths": [
      "multicast",
      "supports_join",
      "lorawan_version",
      "ids.device_id",
      "ids.dev_eui",
      "ids.join_eui",
      "mac_settings.supports_32_bit_f_cnt",
      "supports_class_c",
      "supports_class_b",
      "lorawan_phy_version",
      "frequency_plan_id"
    ]
  }
}
```
Application Server:
```
URL: https://eu1.cloud.thethings.network/api/v3/as/applications/cambridgesensornetwork/devices/test-device-1
{
  "end_device": {
    "ids": {
      "device_id": "test-device-1",
      "dev_eui": "A81758FFFE044BAB",
      "join_eui": "70B3D57ED00358FF"
    }
  },
  "field_mask": {
    "paths": [
      "ids.device_id",
      "ids.dev_eui",
      "ids.join_eui"
    ]
  }
}
```
Also, while registering a device if the registration fails for one server for some reason, it needs to be deleted from all the previously registered servers before a retry.

### Deleting Device
1. V2 had a single delete call.
2. V3 again requires deletion from the four servers in reverse order, Application>Network>Join>Identity