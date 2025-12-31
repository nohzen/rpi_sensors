import os
import time, datetime
import csv
from co2_mh_z19 import Co2SensorMhZ19
from thermometer_adt7410 import adt7410_read
from thermometer_sht31 import HumidityTemperatureSensorSht31
import switchbot


sht31_sensor = HumidityTemperatureSensorSht31()
co2_sensor = Co2SensorMhZ19(serial_device="/dev/ttyS0", abc=False)
switchbot_sensor = switchbot.SwitchBot()


def write_header(csv_path, place):
    with open(csv_path, 'a') as file:
        csv_writer = csv.writer(file)
        # csv_writer.writerow(["datetime",
        #                      "sht31_temperature", "sht31_humidity",
        #                      "adt7410_temperature",
        #                      "mhz19_1_co2", "mhz19_1_temperature",
        #                      "mhz19_2_co2", "mhz19_2_temperature"])
        if place == "home":
            csv_writer.writerow(["datetime",
                                "adt7410_temperature",
                                "mhz19_co2", "mhz19_temperature"])
        elif place == "office":
            csv_writer.writerow(["datetime",
                                "sht31_temperature", "sht31_humidity",
                                "mhz19_co2", "mhz19_temperature"])
        else:
            raise NotImplementedError()


def read_sensor(sensor_db, place):
    now = datetime.datetime.now().isoformat(sep=" ")


    if place == "home":
        adt7410_temperature = adt7410_read()
        mhz19_co2, mhz19_temperature = co2_sensor.readall()
        switchbot_sensor.update_header()
        switchbot_meter_temperature, switchbot_meter_humidity = switchbot_sensor.get_meter()
        switchbot_hub3_temperature, switchbot_hub3_humidity = switchbot_sensor.get_hub3()
        switchbot_outdoor_meter_temperature, switchbot_outdoor_meter_humidity = switchbot_sensor.get_outdoor_meter()

        data_dict = {
            'datetime': now,
            'adt7410_temperature': adt7410_temperature,
            'mhz19_co2': mhz19_co2,
            'mhz19_temperature': mhz19_temperature,
            'switchbot_meter_temperature': switchbot_meter_temperature,
            'switchbot_meter_humidity': switchbot_meter_humidity,
            'switchbot_hub3_temperature': switchbot_hub3_temperature,
            'switchbot_hub3_humidity': switchbot_hub3_humidity,
            'switchbot_outdoor_meter_temperature': switchbot_outdoor_meter_temperature,
            'switchbot_outdoor_meter_humidity': switchbot_outdoor_meter_humidity,
        }
        sensor_db.add_data(data_dict)
    elif place == "office":
        sht31_temperature, sht31_humidity = sht31_sensor.read()
        mhz19_co2, mhz19_temperature = co2_sensor.readall()
        data_dict = {
            'datetime': now,
            'sht31_temperature': sht31_temperature,
            'sht31_humidity': sht31_humidity,
            'mhz19_co2': mhz19_co2,
            'mhz19_temperature': mhz19_temperature
        }
        sensor_db.add_data(data_dict)
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    import argparse
    from database import SensorDataDB

    parser = argparse.ArgumentParser()
    parser.add_argument("--db_path", default="./datas/data.db",
                        help="Path to sqlite db file")
    parser.add_argument("--place", default="office", choices=["office", "home"],
                        help="place to use (determine sensors)")
    args = parser.parse_args()

    db_path = args.db_path
    place = args.place

    sensor_db = SensorDataDB(db_path)

    while True:
        read_sensor(sensor_db, place)
        time.sleep(300.0)
