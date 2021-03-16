# TTN Device Registration Application

This application reads the QR Code on the TTN Device and registers it to the TTN Console.

## Prerequisites
1. This app also stores the Device EUI in a text file on the Android device, so provide **storage permissions** for the app from settings before first use.
2. Internet connectivity is required for the registration process.

## How to use
1. The app supports both single device registration and multiple device registration.
2. On starting the app, you could select either of the two buttons to register a single device or register multiple devices.
3. Register Single Device
   1. Flash the smartphone camera over the device's QR code.
   2. When read correctly, the Device Code and Device EUI will be displayed at the top of the app. Eg: *ERSCO2,EUI:A83527782134543DE*.
   3. A dialog box will appear showing the Device Code and Device EUI and ask for confirmation to register.
   4. Click Yes to register the device.
      1. On successfully registered, a toast message will appear with a vibration cue, notifying that the device has been added. This message will also show the device id.
      2. If device is already registered or if there was some error with registration, a corresponding toast message with vibration will be shown.
   5. Click No to return to Home Screen. The Device Code and Device EUI will be written to the file.
4. Register Multiple Device
   1. Flash the smartphone camera over a device's QR code.
   2. When read correctly, the Device Code and Device EUI will be displayed at the top of the app. Eg: *ERSCO2,EUI:A83527782134543DE*.
   3. No confirmation prompt would be given in this option.
   4. Once registered a toast message will be flashed showing the device_id of the registered device, along with a vibration cue.
   5. If device is already registered or if there was some error with registration, a corresponding toast message with vibration will be shown.
   6. Flash on another device's QR Code to register it.
5. Click the Home Screen button anytime to return to Home Screen.
6. The Device EUIs will be stored in a directory **DevEUI**.

