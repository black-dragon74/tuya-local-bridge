from flask import Flask
import json

import tinytuya

import utils

app = Flask(__name__)

# Store and init tuya device instances
tuya_devices = {}

# Scan for available devices
# local_devices = tinytuya.deviceScan(maxretry=1)
local_devices = json.load(open('snapshot.json', 'r'))['devices']

for device in local_devices:
    m_device = tinytuya.BulbDevice(
        dev_id=device['id'],
        address=device['ip'],
        local_key=device['key'],
        version=device['ver'],
    )
    m_device.set_socketPersistent(True)
    m_device.set_socketNODELAY(True)
    m_device.set_socketRetryLimit(1)
    m_device.set_socketTimeout(2)
    m_device.set_bulb_type('B')
    tuya_devices[device['id']] = m_device


# tinytuya.set_debug(True)


@app.get('/')
def welcome():
    return {
        "msg": "Welcome to the API!"
    }


@app.get('/<dev_id>/on')
def on(dev_id):
    d = tuya_devices.get(dev_id, "")
    if d != "":
        d.turn_on()
        return {
            "status": "OK"
        }
    else:
        return {
            "status": "ERR"
        }


@app.get('/<dev_id>/off')
def off(dev_id):
    d = tuya_devices.get(dev_id, "")
    if d != "":
        d.turn_off()
        return {
            "status": "OK"
        }
    else:
        return {
            "status": "ERR"
        }


@app.get('/<dev_id>/status')
def status(dev_id):
    d = tuya_devices.get(dev_id, "")
    if d == "":
        return {
            "status": "ERR"
        }

    resp = d.status()
    if "Err" in resp:
        return utils.resp_err(resp)
    else:
        return utils.resp_success(resp)


@app.get('/<dev_id>/lux/<int:percent>')
def set_lux(dev_id, percent):
    d = tuya_devices.get(dev_id, "")
    if d == "":
        return {
            "status": "ERR"
        }

    d.turn_on()
    return {
        "percent": percent,
        **d.set_brightness_percentage(percent)
    }


@app.get('/devices')
def list_devices():
    return {
        "status": "OK",
        "devices": [d for d in local_devices]
    }


@app.get('/<dev_id>/power')
def power(dev_id):
    d = tuya_devices.get(dev_id, "")
    if d == "":
        return {
            "status": "ERR"
        }

    return {
        "status": "OK",
        "power": True if d.status()["dps"]["20"] is True else False
    }
