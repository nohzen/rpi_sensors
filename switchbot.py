import time
import hashlib
import hmac
import base64
import uuid
import requests
import json


class SwitchBot():
    def __init__(self):
        self.update_header()

    def update_header(self):
        # Declare empty header dictionary
        apiHeader = {}
        json_path = 'switchbot_setting.json'
        with open(json_path, 'r') as f:
            setting = json.load(f)
        # open token
        token = setting['token']
        # secret key
        secret = setting['secret']

        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        #Build api header JSON
        apiHeader['Authorization']=token
        apiHeader['Content-Type']='application/json'
        apiHeader['charset']='utf8'
        apiHeader['t']=str(t)
        apiHeader['sign']=str(sign, 'utf-8')
        apiHeader['nonce']=str(nonce)
        self.header = apiHeader

    def get_device_list(self):
        header = self.header
        response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=header)
        response_json = response.json()
        body = response_json['body']

        print("deviceList:")
        for device in body['deviceList']:
            print("  id:    ", device['deviceId'])
            print("    type:", device['deviceType'])
            print("    name:", device['deviceName'])
            print("    hub: ", device['hubDeviceId'])

        print("infraredRemoteList:")
        for remote in body['infraredRemoteList']:
            print("  id:    ", remote['deviceId'])
            print("    name:", remote['deviceName'])
            print("    hub: ", remote['hubDeviceId'])

    def get_status(self, device_id):
        header = self.header
        response = requests.get(
            f"https://api.switch-bot.com/v1.1/devices/{device_id}/status",
            headers=header,
        )
        response_json = response.json()
        message = response_json['message']
        if message != "success":
            raise ValueError(f"Failed to get device status. message: {message}")
        status_code = response_json['statusCode']
        if (status_code != 100):
            raise ValueError(f"Failed to get device status. status code: {status_code}, message: {message}")
        body = response_json['body']
        return body

    def get_meter(self):
        device_id = "C2080BE62D9F"
        status = self.get_status(device_id)

        device_id = status['deviceId']
        device_type = status['deviceType']
        hub_device_id = status['hubDeviceId']
        firmware_version = status['version']
        battery = status['battery']
        temperature = status['temperature']
        humidity = status['humidity']
        print(f"[meter] temperature: {temperature}C, humidity: {humidity}%, battery: {battery}%")
        return temperature, humidity

    def get_outdoor_meter(self):
        device_id = "F2B202463828"
        status = self.get_status(device_id)

        device_id = status['deviceId']
        device_type = status['deviceType']
        hub_device_id = status['hubDeviceId']
        firmware_version = status['version']
        battery = status['battery']
        temperature = status['temperature']
        humidity = status['humidity']
        print(f"[outdoor meter] temperature: {temperature}C, humidity: {humidity}%, battery: {battery}%")
        return temperature, humidity

    def get_meter_plus(self):
        device_id = "FD1B69F4FF5E"
        status = self.get_status(device_id)

        device_id = status['deviceId']
        device_type = status['deviceType']
        hub_device_id = status['hubDeviceId']
        firmware_version = status['version']
        battery = status['battery']
        temperature = status['temperature']
        humidity = status['humidity']
        print(f"[meter plus] temperature: {temperature}C, humidity: {humidity}%, battery: {battery}%")
        return temperature, humidity

    def get_hub3(self):
        device_id = "B0E9FEAC35F5"
        status = self.get_status(device_id)

        device_id = status['deviceId']
        device_type = status['deviceType']
        hub_device_id = status['hubDeviceId']
        firmware_version = status['version']
        temperature = status['temperature']
        humidity = status['humidity']
        lightLevel = status['lightLevel'] # [0-10]
        moveDetected = status['moveDetected']
        onlineStatus = status['onlineStatus']
        print(f"[hub3] temperature: {temperature}C, humidity: {humidity}%, lightLevel: {lightLevel}, moveDetected: {moveDetected}, onlineStatus: {onlineStatus}")
        return temperature, humidity

    def get_curtain3(self):
        device_id = "E968105FCF02"
        status = self.get_status(device_id)

        device_id = status['deviceId']
        device_type = status['deviceType']
        hub_device_id = status['hubDeviceId']
        firmware_version = status['version']
        calibrated = status['calibrate']
        group = status['group']
        moving = status['moving']
        battery = status['battery']
        slide_position = status['slidePosition'] # 0%: open, 100%: closed
        print(f"[curtain3] calibrated: {calibrated}, group: {group}, moving: {moving}, battery: {battery}%, slidePosition: {slide_position}%")

    def get_bot(self):
        device_id = "F2B203866749"
        status = self.get_status(device_id)

        device_id = status['deviceId']
        device_type = status['deviceType']
        hub_device_id = status['hubDeviceId']
        firmware_version = status['version']
        power = status['power'] # "on" or "off"
        battery = status['battery']
        deviceMode = status['deviceMode'] # pressMode, switchMode, or customizeMode
        print(f"[bot] power: {power}, battery: {battery}, deviceMode: {deviceMode}")

    def get_ceiling_light(self):
        device_id = "E62BB7AFC7F7"
        status = self.get_status(device_id)

        device_id = status['deviceId']
        device_type = status['deviceType']
        hub_device_id = status['hubDeviceId']
        firmware_version = status['version']
        power = status['power'] # "on" or "off"
        brightness = status['brightness'] # 0-100
        colorTemperature = status['colorTemperature'] # 2700-6500
        # online_status = status['onlineStatus']
        print(f"[ceiling light] power: {power}, brightness: {brightness}, colorTemperature: {colorTemperature}K")

    def send_command(self, device_id, command, parameter="default"):
        header = self.header
        payload = {
            "command": command,
            "parameter": parameter,
            "commandType": "command"
        }
        response = requests.post(
            f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands",
            headers=header,
            json=payload
        )

        response_json = response.json()
        status_code = response_json['statusCode']
        message = response_json['message']
        # body = response_json['body'] # empty
        if (status_code != 100) or (message != "success"):
            raise ValueError(f"Failed to send command. status code: {status_code}, message: {message}")

    def send_bot(self):
        device_id = "F2B203866749"
        # self.send_command(device_id, "turnOn")
        self.send_command(device_id, "turnOff")
        # self.send_command(device_id, "press")

    def send_curtain3(self):
        device_id = "E968105FCF02"
        # self.send_command(device_id, "turnOff") # Close (Position: 100%)
        # self.send_command(device_id, "turnOn") # Open (Position: 0%)
        # self.send_command(device_id, "pause")
        parameter = "0,ff,0" # index, mode, position
        self.send_command(device_id, "setPosition", parameter=parameter)

    def test_api(self):
        # self.get_device_list()

        self.get_meter()
        self.get_meter_plus()
        self.get_outdoor_meter()
        self.get_hub3()
        # self.get_bot()
        # self.get_curtain3()
        # self.get_ceiling_light()

        # self.send_bot()
        # self.send_curtain3()


if __name__ == '__main__':
    switchbot = SwitchBot()
    # switchbot.get_device_list()
    switchbot.get_hub3()
    # switchbot.send_bot()