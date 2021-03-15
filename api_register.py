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
            }
        }
    return device_settings

def register_device(device_settings, app_id):
    manager = ACPTTNManager(settings, app_id)
    response = manager.register_device(device_settings)
    return response

@app.route('/device/', methods=['POST'])
def register():
    app_id = settings['DEFAULT_APPLICATION']
    content = request.json
    if content['access_token'] == settings['ACCESS_TOKEN']:
        qrdata_list = content['qrdata'].strip().split(',')
        if len(qrdata_list) > 2:
            response_list = []
            for device in qrdata_list[1:]:
                deveui_str = qrdata_list[0].split('-')[0]+','+device
                device_settings = get_device_settings(deveui_str)
                response = register_device(device_settings, app_id)
                response_list.append(response+':'+device_settings["ids"]["device_id"])
            response_text = ''
            for resp in response_list:
                resp_list = resp.split(':')
                if resp_list[0] == 'Device added':
                    response_text += 'Added:'+resp_list[1]
                elif resp_list[0] == 'Device updated':
                    response_text += 'Already registered:'+resp_list[1]
                else:
                    response_text += 'Error:'+resp_list[1]
            return jsonify({"response":response, "device":response_text})
        device_settings = get_device_settings(content['qrdata'])
        response = register_device(device_settings, app_id)
        return jsonify({"response":response, "device":device_settings["ids"]["device_id"]})
    else:
        return jsonify({"response":"Can't process request"})

@app.route('/', methods=['GET'])
def home():
    return jsonify('Hello')


settings = load_settings()
settings['host'] = 'localhost'
settings['port'] = 5015
device_keys = {'ERSCO2' : 'elsys-co2', 'ERSEye' : 'elsys-eye', 'EMS' : 'elsys-ems'}

if __name__ == '__main__':
    app.run( host=settings["host"],
             port=settings["port"],
             debug=DEBUG)
