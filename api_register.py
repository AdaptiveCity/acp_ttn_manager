from flask import Flask, json, request, render_template,url_for, redirect, jsonify, make_response
from flask_cors import CORS, cross_origin
from ACPTTNManager import ACPTTNManager

DEBUG = True

app = Flask(__name__)
CORS(app)

def load_settings():
    with open('secrets/settings.json', 'r') as settings_file:
        settings_data = settings_file.read()

    # parse file
    settings = json.loads(settings_data)
    return settings

def get_device_settings(qrdata):
    device_key = qrdata.strip().split(',')[0]
    dev_eui = qrdata.strip().split(':')[-1]
    device_id = device_keys[device_key]+'-'+dev_eui[-6:].lower()
    
    device_settings = {
            "ids": {
                "device_id": device_id,
                "dev_eui": dev_eui
            },            
            "ttn_version": 3
        }
    return device_settings

def register_device(device_settings, app_id):
    manager = ACPTTNManager(settings, app_id)
    response = manager.register_device(device_settings)
    return response

@app.route('/register/', methods=['POST'])
def register():
    app_id = settings['DEFAULT_APPLICATION']
    content = request.json
    device_settings = get_device_settings(content['qrdata'])
    response = register_device(device_settings, app_id)
    return jsonify({"response":response, "device":device_settings["ids"]["device_id"]})

@app.route('/', methods=['GET'])
def home():
    return jsonify('Hello')


settings = load_settings()
settings['host'] = '0.0.0.0'
settings['port'] = 5015
device_keys = {'ERSCO2' : 'elsys-co2', 'ERSEye' : 'elsys-eye', 'ERSEMS' : 'elsys-ems'}        

if __name__ == '__main__':    
    app.run( host=settings["host"],
             port=settings["port"],
             debug=DEBUG)