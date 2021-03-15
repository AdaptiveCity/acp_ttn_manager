# TTN Device Registration Application

This application reads the QR Code on the TTN Device and registers it to the TTN Console.

## Prerequisites
1. This app also stores the Device EUI in a text file on the Android device, so provide storage permissions for the app from settings before first use.
2. Internet connectivity is required for the registration process.

## How to use
1. Start the device and tap on the **Scan QR** button.
2. Flash the smartphone camera over the device's QR code.
3. When read correctly, the Device Code and Device EUI will be displayed at the top of the app. Eg: *ERSCO2,EUI:A83527782134543DE*
4. Once registered a toast message will be flashed showing the device_id of the registered device.
5. On registration failure, the toast message will notify the same.
6. The Device EUIs will be stored in a directory **DevEUI**
