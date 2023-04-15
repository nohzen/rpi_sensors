# -*- coding: utf-8 -*-
"""Humidity and Temperature Sensor SENSIRION SHT31
https://akizukidenshi.com/catalog/g/gK-12125/

SHT31 -- RasPi
================
V+    -- 3.3V (Pin1 or Pin17)
SDA   -- I2C SDA (GPIO 2)
SCL   -- I2C SCL (GPIO 3)
ADR   -- Free or GND
GND   -- GND
"""
from smbus2 import SMBus
import time



class HumidityTemperatureSensorSht31():
    ADDRESS_SHT31 = 0x45 # or 0x44

    def __init__(self):
        self.bus = SMBus(1)

        # 測定モード
        self.mode = "single_shot_mode" # 単発測定: "single_shot_mode", 連続測定: "periodic_data_acquisition_mode"
        # 測定精度
        self.repeatability = "High" # "High" "Medium" "Low"

        self.max_measurement_duration = None # 測定が終わるまでにかかる時間 [ms]
        self.LSB_hex_code = None # write_byte_data で書き込み値
        if self.repeatability == "High":
            self.max_measurement_duration = 15
            self.LSB_hex_code = 0x00
        elif self.repeatability == "Medium":
            self.max_measurement_duration = 6
            self.LSB_hex_code = 0x0B
        elif self.repeatability == "Low":
            self.max_measurement_duration = 4
            self.LSB_hex_code = 0x16
        else:
            raise NotImplementedError(self.repeatability)

        if self.mode == "single_shot_mode":
            pass
        elif self.mode == "periodic_data_acquisition_mode":
            self.bus.write_byte_data(HumidityTemperatureSensorSht31.ADDRESS_SHT31, 0x27, 0x37) # 頻度10mps, 精度高
            time.sleep(0.001) # 命令発行の後は1ms待つ
        else:
            raise NotImplementedError(mode)

    def __del__(self):
        self.bus.close()

    def read(self):
        if self.mode == "single_shot_mode":
            self.bus.write_byte_data(HumidityTemperatureSensorSht31.ADDRESS_SHT31, 0x24, self.LSB_hex_code) # クロックストレッチ無効
            time.sleep(self.max_measurement_duration * 0.001) # 測定が終わるまで待たないとだめ（クロックストレッチを使わないので）
            time.sleep(0.01) # もう少し待たないとエラーになる場合があった
        elif self.mode == "periodic_data_acquisition_mode":
            pass
        else:
            raise NotImplementedError(self.mode)

        data = self.bus.read_i2c_block_data(HumidityTemperatureSensorSht31.ADDRESS_SHT31, 0x00, 6)
        time.sleep(0.001)

        temperature = 0.0026702880 * ((data[0] << 8) | data[1]) - 45
        humidity = 0.0015258789 * ((data[3] << 8) | data[4])
        # temperature = 175 * ((data[0] << 8) | data[1]) / 65535.0 - 45
        # humidity = 100 * ((data[3] << 8) | data[4]) / 65535.0

        return temperature, humidity # [C] [%RH]


if __name__ == '__main__':
    import datetime

    sensor = HumidityTemperatureSensorSht31()

    try:
        while True:
            temperature, humidity = sensor.read()
            now = datetime.datetime.now()

            print("{0}: temperature = {1:03.1f} [C], humidity = {2:03.1f} [%RH]".format(now, temperature, humidity))
            time.sleep(10.0)
    except KeyboardInterrupt:
        pass
